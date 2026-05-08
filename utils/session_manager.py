import os
import pickle
import json
import time
import logging
from urllib.parse import urlparse
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils.logger_config import logger

class SessionManager:
    def __init__(
        self,
        driver,
        session_dir="session_data",
        app_base_url="https://app.brightcone.ai",
        dashboard_url="https://app.brightcone.ai/dashboard",
        session_max_age_seconds=8 * 60 * 60,
    ):
        self.driver = driver
        self.session_dir = session_dir
        self.app_base_url = app_base_url
        self.dashboard_url = dashboard_url
        self.session_max_age_seconds = session_max_age_seconds
        self.cookies_file = os.path.join(self.session_dir, "cookies.pkl")
        self.local_storage_file = os.path.join(self.session_dir, "local_storage.json")
        self.session_storage_file = os.path.join(self.session_dir, "session_storage.json")
        self.metadata_file = os.path.join(self.session_dir, "session_metadata.json")
        
        if not os.path.exists(self.session_dir):
            os.makedirs(self.session_dir)
            logger.info(f"Created session directory: {self.session_dir}")

    def _save_session_metadata(self, cookie_count):
        metadata = {
            "saved_at": time.time(),
            "cookie_count": cookie_count,
        }
        with open(self.metadata_file, "w") as f:
            json.dump(metadata, f)

    def _is_session_fresh(self):
        if not os.path.exists(self.metadata_file):
            logger.warning("Session metadata missing. Treating saved session as stale.")
            return False

        try:
            with open(self.metadata_file, "r") as f:
                metadata = json.load(f)
            saved_at = float(metadata.get("saved_at", 0))
            age_seconds = time.time() - saved_at
            is_fresh = age_seconds <= self.session_max_age_seconds
            logger.info(
                f"Saved session age: {round(age_seconds, 2)}s "
                f"(max allowed {self.session_max_age_seconds}s). Fresh={is_fresh}"
            )
            return is_fresh
        except Exception as metadata_error:
            logger.warning(f"Unable to read session metadata: {metadata_error}")
            return False

    def _restore_storage_file(self, file_path, storage_name):
        if not os.path.exists(file_path):
            logger.info(f"{storage_name} file not found. Skipping restore.")
            return

        with open(file_path, "r") as f:
            storage_data = f.read() or "{}"

        self.driver.execute_script(
            """
            var data = JSON.parse(arguments[0]);
            for (var key in data) {
                window.%s.setItem(key, data[key]);
            }
            return Object.keys(data);
            """
            % storage_name,
            storage_data,
        )
        logger.info(f"{storage_name} restored successfully.")

    def _log_auth_storage_debug(self):
        local_storage_items = self.driver.execute_script(
            """
            var out = {};
            for (var i = 0; i < window.localStorage.length; i++) {
                var k = window.localStorage.key(i);
                out[k] = window.localStorage.getItem(k);
            }
            return out;
            """
        )
        session_storage_items = self.driver.execute_script(
            """
            var out = {};
            for (var i = 0; i < window.sessionStorage.length; i++) {
                var k = window.sessionStorage.key(i);
                out[k] = window.sessionStorage.getItem(k);
            }
            return out;
            """
        )
        logger.info(f"localStorage keys after restore: {list(local_storage_items.keys())}")
        logger.info(f"sessionStorage keys after restore: {list(session_storage_items.keys())}")

    def wait_for_authenticated_dashboard(self, timeout=20):
        try:
            WebDriverWait(self.driver, timeout).until(
                lambda d: "login" not in (d.current_url or "").lower()
            )
            WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((By.TAG_NAME, "aside"))
            )
            WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located(
                    (By.XPATH, "//span[contains(text(),'Dashboard')]")
                )
            )
            logger.info("Authenticated dashboard element detected.")
            return True
        except Exception as wait_error:
            try:
                self.driver.save_screenshot("session_failure.png")
            except Exception:
                pass
            logger.warning(
                f"Dashboard authentication element not found within {timeout}s: {wait_error}"
            )
            return False

    def save_session(self):
        """
        Captures and stores browser session data including cookies, localStorage, and sessionStorage.
        """
        try:
            # Save cookies using CDP first (captures broader cookie scope than get_cookies()).
            cookies = []
            try:
                self.driver.execute_cdp_cmd("Network.enable", {})
                cdp_result = self.driver.execute_cdp_cmd("Network.getAllCookies", {})
                cookies = cdp_result.get("cookies", []) or []
                logger.info(f"Captured {len(cookies)} cookies using CDP.")
            except Exception as cdp_error:
                logger.warning(f"CDP cookie capture failed, falling back to WebDriver cookies: {cdp_error}")
                cookies = self.driver.get_cookies()

            with open(self.cookies_file, "wb") as f:
                pickle.dump(cookies, f)
            
            # Save Local Storage
            local_storage = self.driver.execute_script("return JSON.stringify(window.localStorage);")
            with open(self.local_storage_file, "w") as f:
                f.write(local_storage)
                
            # Save Session Storage
            session_storage = self.driver.execute_script("return JSON.stringify(window.sessionStorage);")
            with open(self.session_storage_file, "w") as f:
                f.write(session_storage)

            self._save_session_metadata(len(cookies))
            
            logger.info("Session data (cookies, localStorage, sessionStorage) saved successfully.")
            if not cookies:
                logger.warning("No cookies were captured. Session restore may not work for auth flows.")
        except Exception as e:
            logger.error(f"Failed to save session data: {e}")

    def load_session(self):
        """
        Loads cookies, localStorage, and sessionStorage into the browser.
        """
        if not os.path.exists(self.cookies_file):
            logger.warning("Session files not found.")
            return False
        if not self._is_session_fresh():
            logger.warning("Saved session is stale or metadata missing. Skipping restore.")
            return False

        try:
            logger.info("Opening base app domain before restoring cookies...")
            self.driver.get(self.app_base_url)
            time.sleep(3)
            WebDriverWait(self.driver, 15).until(
                lambda d: "app.brightcone.ai" in (d.current_url or "").lower()
            )

            # Load Cookies
            with open(self.cookies_file, "rb") as f:
                cookies = pickle.load(f)
                restored = 0
                total = len(cookies)

                for cookie in cookies:
                    cookie_name = cookie.get("name", "<unknown>")
                    cookie_domain = cookie.get("domain", "<unknown-domain>")
                    try:
                        # CDP cookie schema: expires/httpOnly/sameSite...
                        if "expires" in cookie or "httpOnly" in cookie:
                            domain = (cookie.get("domain") or "").lstrip(".")
                            path = cookie.get("path") or "/"
                            secure = bool(cookie.get("secure", True))
                            if domain:
                                scheme = "https" if secure else "http"
                                cookie_url = f"{scheme}://{domain}{path}"
                            else:
                                current = self.driver.current_url or "https://app.brightcone.ai/"
                                parsed = urlparse(current)
                                cookie_url = f"{parsed.scheme}://{parsed.netloc}{path}"

                            cdp_cookie = {
                                "name": cookie.get("name"),
                                "value": cookie.get("value"),
                                "url": cookie_url,
                                "domain": cookie.get("domain"),
                                "path": path,
                                "secure": secure,
                                "httpOnly": bool(cookie.get("httpOnly", False)),
                            }
                            if cookie.get("expires") is not None and cookie.get("expires") > 0:
                                cdp_cookie["expires"] = float(cookie.get("expires"))
                            same_site = cookie.get("sameSite")
                            if same_site in {"Strict", "Lax", "None"}:
                                cdp_cookie["sameSite"] = same_site

                            result = self.driver.execute_cdp_cmd("Network.setCookie", cdp_cookie)
                            if result.get("success"):
                                restored += 1
                                logger.info(
                                    f"Cookie restored via CDP: name={cookie_name}, domain={cookie_domain}, result=success"
                                )
                            else:
                                logger.warning(
                                    f"Cookie restore failed via CDP: name={cookie_name}, domain={cookie_domain}, result={result}"
                                )
                        else:
                            # WebDriver cookie schema: expiry/... (same-domain only)
                            if "expiry" in cookie:
                                cookie["expiry"] = int(cookie["expiry"])
                            self.driver.add_cookie(cookie)
                            restored += 1
                            logger.info(
                                f"Cookie restored via WebDriver: name={cookie_name}, domain={cookie_domain}, result=success"
                            )
                    except Exception as e:
                        logger.warning(
                            f"Could not restore cookie name={cookie_name}, domain={cookie_domain}. Exception: {e}"
                        )

                logger.info(f"Restored {restored}/{total} cookies into browser.")
            
            # Load Local Storage
            self._restore_storage_file(self.local_storage_file, "localStorage")
            
            # Load Session Storage
            self._restore_storage_file(self.session_storage_file, "sessionStorage")
            self._log_auth_storage_debug()

            # Refresh once so app boots with restored state.
            try:
                self.driver.refresh()
                WebDriverWait(self.driver, 20).until(
                    lambda d: d.execute_script("return document.readyState") == "complete"
                )
                WebDriverWait(self.driver, 20).until(
                    EC.presence_of_element_located((By.TAG_NAME, "aside"))
                )
                logger.info("Browser refresh complete after session restore.")
            except Exception as refresh_error:
                logger.warning(f"Browser refresh after session load failed: {refresh_error}")
                try:
                    self.driver.save_screenshot("session_failure.png")
                except Exception:
                    pass

            logger.info(f"Post-restore URL: {self.driver.current_url}")
            logger.info(f"Post-restore title: {self.driver.title}")
            logger.info(f"Post-restore cookies count in browser: {len(self.driver.get_cookies())}")
            logger.info(
                "LocalStorage keys: %s",
                self.driver.execute_script("return Object.keys(window.localStorage);"),
            )
            logger.info(
                "SessionStorage keys: %s",
                self.driver.execute_script("return Object.keys(window.sessionStorage);"),
            )
            
            logger.info("Session data loaded into browser.")
            return True
        except Exception as e:
            logger.error(f"Failed to load session data: {e}")
            return False

    def is_session_valid(self, dashboard_url=None):
        """
        Checks if the session is still valid.
        """
        dashboard_url = dashboard_url or self.dashboard_url
        try:
            logger.info(f"Validating session at {dashboard_url}...")
            self.driver.get(dashboard_url)
            WebDriverWait(self.driver, 20).until(
                lambda d: d.execute_script("return document.readyState") == "complete"
            )
            
            current_url = self.driver.current_url
            logger.info(f"Current URL: {current_url}")
            
            if "login" in current_url.lower():
                try:
                    self.driver.save_screenshot("session_failure.png")
                except Exception:
                    pass
                logger.warning("Session invalid: Redirected to login.")
                return False

            if self.wait_for_authenticated_dashboard(timeout=20):
                logger.info("Session validated via authenticated dashboard element.")
                return True

            try:
                self.driver.save_screenshot("session_failure.png")
            except Exception:
                pass
            logger.warning("Session invalid: dashboard authenticated element was not found.")
            return False
        except Exception as e:
            logger.error(f"Validation error: {e}")
            return False
