import os
import time
from datetime import datetime
from utils.logger_config import logger
from utils.data_reader import DataReader
from base.webdriver_factory import WebDriverFactory
from pages.login_page import LoginPage
from pages.otp_page import OTPPage
from pages.recruitment_page import RecruitmentPage
from pages.documents_page import DocumentsPage
from utils.gmail_util import GmailUtil
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
    logger.info(f"Selected Browser for Run: {context.browser_name.upper()}")
    
    # 6. Initialize Utils
    context.gmail_util = GmailUtil(context.current_user["email"], "linx lpbq ljjj widk")

def before_scenario(context, scenario):
    EXECUTION_STATS["total"] += 1
    logger.info(f"Scenario: {scenario.name} - STARTED")
    
    # 7. Initialize WebDriver for each scenario
    factory = WebDriverFactory(browser_name=context.browser_name)
    context.driver = factory.get_driver()
    context.driver.implicitly_wait(context.timeout)

    # 8. Initialize Page Objects
    context.login_page = LoginPage(context.driver)
    context.otp_page = OTPPage(context.driver)
    context.recruitment_page = RecruitmentPage(context.driver)
    context.documents_page = DocumentsPage(context.driver)
    
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
