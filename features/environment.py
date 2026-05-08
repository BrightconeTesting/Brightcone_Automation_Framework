import os
import time
<<<<<<< HEAD
import logging
from datetime import datetime
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
=======
from datetime import datetime
from utils.logger_config import logger
from utils.data_reader import DataReader
from base.webdriver_factory import WebDriverFactory
>>>>>>> a47c1fe2ef3455fd6c1379e7bfde553d708c9201
from pages.login_page import LoginPage
from pages.otp_page import OTPPage
from pages.recruitment_page import RecruitmentPage
from pages.documents_page import DocumentsPage
from utils.gmail_util import GmailUtil
<<<<<<< HEAD
from base.webdriver_factory import WebDriverFactory
from utils.logger_config import logger
from utils.session_manager import SessionManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import allure
from allure_commons.types import AttachmentType

# Session strategy flags
USE_PROFILE_SESSION = True
USE_MANUAL_SESSION_RESTORE = False

# Global counters for reliable summary reporting
EXECUTION_STATS = {
    "total": 0,
    "passed": 0,
    "failed": 0,
    "skipped": 0,
    "start_time": 0
}

def before_all(context):
    """
    Setup logging and initialize browser before tests.
    """
    logger.info("Initializing global test configuration...")
    
    # Initialize counts for summary dashboard
    EXECUTION_STATS["start_time"] = time.time()
    
    # Create screenshots directory if needed
    if not os.path.exists("screenshots"):
        os.makedirs("screenshots")
        logger.info("Created 'screenshots' directory.")

    # Initialize WebDriver
    logger.info("Launching Chrome browser...")
    try:
        context.driver_factory = WebDriverFactory(browser_name="chrome")
        if USE_PROFILE_SESSION:
            # Use a persistent Chrome profile so authenticated browser state survives across runs.
            profile_dir = os.path.abspath(os.path.join("session_data", "chrome_profile"))
            if not os.path.exists(profile_dir):
                os.makedirs(profile_dir)
            context.driver = context.driver_factory.get_driver(user_data_dir=profile_dir)
            logger.info("Session strategy: PROFILE persistence enabled.")
        else:
            context.driver = context.driver_factory.get_driver()
            logger.info("Session strategy: Stateless browser (no profile persistence).")

        logger.info(
            f"Manual serialized restore enabled: {USE_MANUAL_SESSION_RESTORE}"
        )
        logger.info("Browser launched successfully.")
    except Exception as e:
        logger.error(f"Failed to launch browser: {str(e)}")
        raise e
    
    # Initialize Page Objects and Utilities
=======
import allure
from allure_commons.types import AttachmentType

from utils.path_util import PathUtil

# Global execution stats
EXECUTION_STATS = {"total": 0, "passed": 0, "failed": 0, "skipped": 0, "start_time": 0}

def before_all(context):
    """
    Setup environment, roles, and load global configuration.
    """
    logger.info("Initializing framework configuration...")
    EXECUTION_STATS["start_time"] = time.time()
    
    # 1. Load Data from JSON using PathUtil
    config_path = PathUtil.get_config_file("test_config.json")
    context.test_config = DataReader.read_json(config_path)
    
    # 2. Handle Environment from Command Line (-D env=Prod / Staging)
    env_input = context.config.userdata.get("env", "Staging")
    context.env_name = next((k for k in context.test_config["environments"] if k.lower() == env_input.lower()), env_input)
    
    if context.env_name not in context.test_config["environments"]:
        available_envs = list(context.test_config["environments"].keys())
        raise ValueError(f"Environment '{env_input}' not defined. Available: {available_envs}")
    
    env_config = context.test_config["environments"][context.env_name]
    context.base_url = env_config["base_url"]
    context.timeout = env_config["timeout"]
    logger.info(f"Target Environment: {context.env_name.upper()} | URL: {context.base_url}")
    
    # 3. Handle Role from Command Line (-D role=admin / user)
    role_input = context.config.userdata.get("role", "admin")
    context.role_name = next((r for r in context.test_config["roles"] if r.lower() == role_input.lower()), role_input)
    
    if context.role_name not in context.test_config["roles"]:
        available_roles = list(context.test_config["roles"].keys())
        raise ValueError(f"Role '{role_input}' not defined. Available: {available_roles}")
    
    context.current_user = context.test_config["roles"][context.role_name]
    logger.info(f"Current Execution Role: {context.role_name.upper()}")
    
    # 4. Handle Browser from Command Line (-D browser=chrome / firefox / edge)
    context.browser_name = context.config.userdata.get("browser", "chrome")
    
    # 5. Handle Headless Mode (-D headless=true/false) - Defaults to TRUE
    headless_input = context.config.userdata.get("headless", "false").lower()
    context.headless = headless_input == "true"
    
    logger.info(f"Selected Browser for Run: {context.browser_name.upper()} | Headless: {context.headless}")
    
    # 6. Initialize Utils
    context.gmail_util = GmailUtil(context.current_user["email"], context.current_user["app_password"])

def before_scenario(context, scenario):
    EXECUTION_STATS["total"] += 1
    logger.info(f"Scenario: {scenario.name} - STARTED")
    
    # 7. Initialize WebDriver for each scenario
    factory = WebDriverFactory(browser_name=context.browser_name, headless=context.headless)
    context.driver = factory.get_driver()

    context.driver.implicitly_wait(context.timeout)

    # 8. Initialize Page Objects
>>>>>>> a47c1fe2ef3455fd6c1379e7bfde553d708c9201
    context.login_page = LoginPage(context.driver)
    context.otp_page = OTPPage(context.driver)
    context.recruitment_page = RecruitmentPage(context.driver)
    context.documents_page = DocumentsPage(context.driver)
    
<<<<<<< HEAD
    context.email_address = "munjalaharikrishna123@gmail.com"
    context.app_password = "linx lpbq ljjj widk"
    context.gmail_util = GmailUtil(context.email_address, context.app_password)

    # --- SESSION PERSISTENCE LOGIC ---
    context.session_manager = SessionManager(context.driver)

    is_valid = False

    # 1. Attempt profile session reuse first when enabled.
    if USE_PROFILE_SESSION:
        logger.info("Attempting to reuse profile-based authenticated session...")
        is_valid = context.session_manager.is_session_valid()
        if is_valid:
            logger.info("Profile session reused successfully.")
        else:
            logger.warning("Profile session not valid.")

    # 2. Attempt manual restore only when explicitly enabled.
    if not is_valid and USE_MANUAL_SESSION_RESTORE:
        logger.info("Attempting serialized session restore from saved artifacts...")
        session_loaded = context.session_manager.load_session()
        if session_loaded:
            logger.info("Session artifacts restored. Validating authenticated state...")
            is_valid = context.session_manager.is_session_valid()
        else:
            logger.warning("Serialized restore could not be completed.")

    # 3. Fallback Login if needed
    if not is_valid:
        logger.info("Session is missing or invalid. Triggering full login flow...")
        try:
            # Re-navigate to login if not already there or if redirect happened
            context.login_page.open()
            context.login_page.enter_email(context.email_address)
            context.login_page.click_continue()
            
            logger.info("Waiting for OTP...")
            time.sleep(10) # Time for Gmail to receive OTP
            otp = context.gmail_util.get_otp_from_gmail(timeout=60, retry_interval=5)
            
            if not otp:
                raise Exception("Failed to fetch OTP during persistent login flow.")
            
            context.otp_page.enter_otp(otp)
            context.otp_page.click_login()
            
            # Wait for login processing to complete by checking URL
            logger.info("Waiting for login to complete (URL change)...")
            WebDriverWait(context.driver, 15).until(lambda d: "login" not in d.current_url.lower())

            # Wait for authenticated dashboard shell in SPA before persisting.
            if context.session_manager.wait_for_authenticated_dashboard(timeout=25):
                logger.info("Dashboard loaded after OTP login.")
            else:
                logger.warning("Dashboard shell not detected immediately after OTP login.")

            if context.session_manager.is_session_valid():
                logger.info("Login successful. Saving new session data...")
                context.session_manager.save_session()
            else:
                logger.error("Login performed but validation failed. Check if account has correct permissions.")
        except Exception as e:
            logger.error(f"Auto-login failed: {e}")
    else:
        logger.info("Reusing existing valid session. Ensuring dashboard navigation...")
        context.driver.get("https://app.brightcone.ai/dashboard")
        WebDriverWait(context.driver, 20).until(
            lambda d: d.execute_script("return document.readyState") == "complete"
        )
        context.session_manager.wait_for_authenticated_dashboard(timeout=20)

def before_feature(context, feature):
    """
    Log start of feature.
    """
    logger.info(f"--- START FEATURE: {feature.name} ---")

def before_scenario(context, scenario):
    """
    Log start of scenario and ensure we are on the dashboard/base state.
    """
    EXECUTION_STATS["total"] += 1
    logger.info(f"Scenario: {scenario.name} - Status: STARTED")
    
    # Maintain test independence by resetting navigation state to dashboard
    try:
        current_url = context.driver.current_url
        if "login" not in current_url:
            logger.info("Resetting navigation to dashboard for clean scenario state...")
            context.driver.get("https://app.brightcone.ai/dashboard")
    except Exception as e:
        logger.warning(f"Could not reset state before scenario: {e}")

def before_step(context, step):
    """
    Log each step.
    """
    logger.info(f"  Step: {step.step_type.upper()} {step.name}")

def after_step(context, step):
    """
    Log step status and capture screenshot on failure.
    """
    if step.status == "passed":
        logger.info(f"  Step: {step.name} - Status: PASSED")
    elif step.status == "failed":
        logger.error(f"  Step: {step.name} - Status: FAILED")
        import traceback
        error_details = "".join(traceback.format_exception(type(step.exception), step.exception, step.exc_traceback))
        logger.error(f"  Error Traceback:\n{error_details}")
        
        # Capture screenshot for failure
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_step_name = step.name.replace(" ", "_")[:50]
        screenshot_path = os.path.join("screenshots", f"FAILED_{safe_step_name}_{timestamp}.png")
        
        try:
            context.driver.save_screenshot(screenshot_path)
            logger.info(f"  Screenshot saved at: {screenshot_path}")
            
            # Attach to Allure report
            allure.attach(
                context.driver.get_screenshot_as_png(),
                name=f"FAILED_{safe_step_name}",
                attachment_type=AttachmentType.PNG
            )
            logger.info("  Screenshot attached to Allure report.")
        except Exception as e:
            logger.error(f"  Failed to capture/attach screenshot: {str(e)}")

def after_scenario(context, scenario):
    """
    Log scenario result and update totals.
    """
    if scenario.status.name == "passed":
        EXECUTION_STATS["passed"] += 1
        logger.info(f"Scenario: {scenario.name} - Status: PASSED\n")
    elif scenario.status.name == "failed":
        EXECUTION_STATS["failed"] += 1
        logger.error(f"Scenario: {scenario.name} - Status: FAILED\n")
    else:
        EXECUTION_STATS["skipped"] += 1
        logger.warning(f"Scenario: {scenario.name} - Status: SKIPPED\n")

def after_feature(context, feature):
    """
    Log end of feature.
    """
    logger.info(f"--- END FEATURE: {feature.name} ---")

def after_all(context):
    """
    Finalize reporting and close browser.
    """
    end_time = time.time()
    total_time_seconds = round(end_time - EXECUTION_STATS["start_time"], 2)
    overall_status = "PASS" if EXECUTION_STATS["failed"] == 0 else "FAIL"

    # Console Summary Dashboard (Targeted Scope Only)
    logger.info("-" * 50)
    logger.info(" RUNTIME TEST EXECUTION SUMMARY (TARGETED SCOPE) ")
    logger.info("-" * 50)
    logger.info(f"  Scenarios Selected  : {EXECUTION_STATS['total']}")
    logger.info(f"  Scenarios Passed    : {EXECUTION_STATS['passed']}")
    logger.info(f"  Scenarios Failed    : {EXECUTION_STATS['failed']}")
    logger.info(f"  Scenarios Skipped   : {EXECUTION_STATS['skipped']}")
    logger.info(f"  Total Run Time      : {total_time_seconds}s")
    logger.info(f"  Overall Status      : {overall_status}")
    logger.info("-" * 50)

    # Cleanup
    if hasattr(context, "driver"):
        logger.info("Quitting browser in 10 seconds (for debugging)...")
        time.sleep(10) # Added pause so you can see why it failed
        context.driver.quit()
        time.sleep(1)

    # Automatically generate Allure report if results exist
    if os.path.exists("reports/allure-results"):
        logger.info("Automatically generating Allure HTML report with History and Environment data...")
        try:
            import subprocess
            import shutil
            import platform

            # 1. Create Environment Properties for Allure Dashboard
            env_props_path = os.path.join("reports/allure-results", "environment.properties")
            with open(env_props_path, "w") as f:
                f.write(f"OS={platform.system()} {platform.release()}\n")
                f.write(f"Python_Version={platform.python_version()}\n")
                f.write(f"Browser=Chrome\n")
                f.write(f"Environment=Production\n")

            # 2. Add Executor Details
            executor_path = os.path.join("reports/allure-results", "executor.json")
            with open(executor_path, "w") as f:
                import json
                executor_data = {
                    "name": "Local Machine",
                    "type": "terminal",
                    "buildName": f"Run_{datetime.now().strftime('%Y%m%d_%H%M')}"
                }
                json.dump(executor_data, f)

            # 3. Add Custom Categories for Failure Grouping
            categories_path = os.path.join("reports/allure-results", "categories.json")
            with open(categories_path, "w") as f:
                categories_data = [
                    {"name": "Assertion Failures", "matchedStatuses": ["failed"], "messageRegex": ".*ASSERT.*"},
                    {"name": "Infrastructure/Timeout Issues", "matchedStatuses": ["broken"], "messageRegex": ".*timeout.*"},
                    {"name": "Ignored/Skipped Scenarios", "matchedStatuses": ["skipped"]}
                ]
                json.dump(categories_data, f)

            # 4. Support for TRENDS: Copy history from previous report to current results
            history_dir = os.path.join("reports/allure-report", "history")
            target_history_dir = os.path.join("reports/allure-results", "history")
            if os.path.exists(history_dir):
                shutil.copytree(history_dir, target_history_dir)
                logger.info("Preserved execution history for Trends.")
            
            # Ensure reports directory exists
            if not os.path.exists("reports"):
                os.makedirs("reports")
            
            # 5. Generate the report
            subprocess.run(
                ["allure", "generate", "reports/allure-results", "--clean", "-o", "reports/allure-report"],
                shell=True,
                check=False
            )
            logger.info("Allure report generated in: reports/allure-report")

            # Clean up the JSON results folder after successful generation
            if os.path.exists("reports/allure-results"):
                shutil.rmtree("reports/allure-results")
                logger.info("Cleaned up raw JSON results folder.")
            
            logger.info("To view, run: allure open reports/allure-report")
        except Exception as e:
            logger.warning(f"Failed to auto-generate Allure report. Ensure Allure CLI is installed: {e}")
=======
    # 9. Load Scenario-Specific Data from Excel using PathUtil
    try:
        excel_path = PathUtil.get_excel_file("recruitment_data.xlsx")
        all_excel_data = DataReader.read_excel_data(excel_path)
        context.test_data = DataReader.get_scenario_data(all_excel_data, scenario.name, context.role_name)
        logger.info(f"Test data loaded for scenario: {scenario.name}")
    except Exception as e:
        logger.warning(f"Could not load specific Excel data for scenario: {e}")
        context.test_data = {}

def after_scenario(context, scenario):
    if hasattr(context, "driver"):
        context.driver.quit()
    
    if scenario.status == "failed":
        EXECUTION_STATS["failed"] += 1
    else:
        EXECUTION_STATS["passed"] += 1

def after_step(context, step):
    if step.status == "failed":
        logger.error(f"Step '{step.name}' FAILED")
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        root = PathUtil.get_project_root()
        screenshot_dir = os.path.join(root, "screenshots")
        screenshot_path = os.path.join(screenshot_dir, f"FAILED_{timestamp}.png")
        if not os.path.exists(screenshot_dir): os.makedirs(screenshot_dir)
        context.driver.save_screenshot(screenshot_path)
        allure.attach(context.driver.get_screenshot_as_png(), name="Failure_Screenshot", attachment_type=AttachmentType.PNG)


def after_all(context):
    logger.info("Test execution completed.")
    total_time = time.time() - EXECUTION_STATS["start_time"]
    logger.info(f"Total Execution Time: {total_time:.2f}s")
>>>>>>> a47c1fe2ef3455fd6c1379e7bfde553d708c9201
