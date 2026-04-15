import os
import time
import logging
from datetime import datetime
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from pages.login_page import LoginPage
from pages.otp_page import OTPPage
from pages.recruitment_page import RecruitmentPage
from pages.documents_page import DocumentsPage
from utils.gmail_util import GmailUtil
from base.webdriver_factory import WebDriverFactory
from utils.logger_config import logger
from utils.data_reader import DataReader
import allure
from allure_commons.types import AttachmentType

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
        context.driver = context.driver_factory.get_driver()
        logger.info("Browser launched successfully.")
    except Exception as e:
        logger.error(f"Failed to launch browser: {str(e)}")
        raise e
    
    # Initialize Page Objects and Utilities
    context.login_page = LoginPage(context.driver)
    context.otp_page = OTPPage(context.driver)
    context.recruitment_page = RecruitmentPage(context.driver)
    context.documents_page = DocumentsPage(context.driver)
    
    context.email_address = "munjalaharikrishna123@gmail.com"
    context.app_password = "linx lpbq ljjj widk"
    context.gmail_util = GmailUtil(context.email_address, context.app_password)

    # Initialize Test Data
    logger.info("Loading test data...")
    try:
        context.json_data = DataReader.read_json("test_data/test_config.json")
        context.excel_data = DataReader.read_excel("test_data/test_data_excel.xlsx")
        logger.info("Test data loaded successfully.")
    except Exception as e:
        logger.error(f"Failed to load test data: {str(e)}")

def before_feature(context, feature):
    """
    Log start of feature.
    """
    logger.info(f"--- START FEATURE: {feature.name} ---")

def before_scenario(context, scenario):
    """
    Log start of scenario and increment counts.
    """
    EXECUTION_STATS["total"] += 1
    logger.info(f"Scenario: {scenario.name} - Status: STARTED")

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
