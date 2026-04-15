# Bright Automation Framework Documentation

## 🚀 Framework Overview
**Bright_Automation** is a professional-grade, high-performance BDD (Behavior Driven Development) automation framework built using **Python**, **Selenium**, and **Behave**. It follows the **Page Object Model (POM)** design pattern to ensure scalability, maintainability, and clean code separation.

### 🛠️ Technology Stack
- **Language**: Python 3.11
- **BDD Tool**: Behave (Gherkin syntax)
- **Web Automation**: Selenium WebDriver
- **Browser Management**: WebDriver Manager (Chrome)
- **Reporting**: Allure Reports & Behave HTML Formatter
- **Utilities**: 
  - `imap-tools` (Gmail OTP extraction)
  - `pyautogui` & `pyperclip` (OS-level file upload automation)
  - `python-dotenv` (Environment configuration)
  - `logging` (Customized colored logging)


## 📂 Project Structure
```text
Bright_Automation/
├── base/                   # Core base classes
│   ├── base_page.py        # Common element interactions (click, find, wait)
│   └── webdriver_factory.py# WebDriver initialization & configuration
├── features/               # Gherkin feature files
│   ├── login.feature       # Login & OTP scenarios
│   ├── recruitment.feature # Candidate management scenarios
│   ├── documents.feature   # Document upload scenarios
│   ├── steps/              # Step definition implementation (Python)
│   └── environment.py      # Global hooks (Setup/Teardown, Logging, Reporting)
├── pages/                  # Page Object Model (POM) implementation
│   ├── login_page.py       # Login screens and locators
│   ├── otp_page.py         # OTP screen handling
│   ├── recruitment_page.py # Recruitment dashboard and forms
│   └── documents_page.py   # Document upload section logic
├── utils/                  # Reusable utility modules
│   ├── gmail_util.py       # OTP retrieval from Gmail via IMAP
│   └── logger_config.py    # Standardized logging configuration
├── reports/                # Generated Allure & HTML reports
├── logs/                   # Execution logs
├── screenshots/            # Failure screenshots
├── requirements.txt        # Project dependencies
└── run_allure_report.bat   # Batch script for execution & reporting
```

---

## 🏗️ Core Components

### 1. Base Layer (`base/`)
- **`base_page.py`**: A wrapper for Selenium's native commands. It includes explicit waits (Fluent/Explicit), robust click handling (Standard/JavaScript), and screenshot captures.
- **`webdriver_factory.py`**: Simplifies driver creation. Automatically handles driver binaries and configures browser options (Headless, Window size, Sandbox).

### 2. Page Object Model (`pages/`)
Each UI page has a corresponding Python class. 
- **Locators**: Stored as private variables for easy updates.
- **Actions**: Methods that perform business logic (e.g., `enter_otp()`, `upload_file()`).

### 3. Smart Utilities (`utils/`)
- **Gmail Utility**: Uses `imap-tools` to connect to Gmail, search for recent OTP emails, and extract the code using regex. Perfect for bypassing 2FA.
- **Logger**: Provides real-time execution visibility with timestamps, severity levels, and specific context.

---

## 🧪 Behavior Driven Development (BDD)

### Feature Files
Written in human-readable Gherkin syntax. Examples:
- **Login**: Handles both simple login and 2FA OTP flows.
- **Recruitment**: Validates the end-to-end flow of adding candidates and status transitions.
- **Documents**: Tests the complex multi-category file upload section.

### Environment Hooks (`environment.py`)
This is the "Brain" of the framework. It manages lifecycle events:
- **`before_all`**: Loads browser, initializes page objects, and sets up logging.
- **`before_scenario`**: Resets counters and logs metadata.
- **`after_step`**: 
    - ✅ **Success**: Logs step completion.
    - ❌ **Failure**: Captures a screenshot AND attaches it directly to the Allure report metadata.
- **`after_all`**: Finalizes execution, generates the summary dashboard, and triggers report generation.

---

## 📁 Key Multi-Section Implementations

### Section A: OTP Authentication
1. User enters credentials.
2. Framework waits for the OTP screen.
3. `GmailUtil` connects to the inbox and fetches the latest OTP.
4. Framework enters the code and navigates to the dashboard.

### Section B: Candidate Recruitment
- **Form Filling**: Handles dynamic dropdowns, text inputs, and date pickers.
- **Verification**: Uses explicit waits to ensure the candidate list is updated before assertion.

### Section C: OS-Level File Uploads
Since Selenium cannot interact with standard Windows File Explorer dialogs:
1. Framework clicks "Upload".
2. **`pyperclip`** copies the absolute file path.
3. **`pyautogui`** simulates keyboard shortcuts (`Ctrl+V` and `Enter`) to confirm the upload.
4. Framework then validates the "Success" toast notification or UI update.

---

## 📊 Report Section

The framework provides multi-dimensional reporting to satisfy both developers and stakeholders.

### 1. Console Execution Summary
At the end of every run, a "Summary Dashboard" is printed to the terminal:
```text
--------------------------------------------------
 RUNTIME TEST EXECUTION SUMMARY (TARGETED SCOPE) 
--------------------------------------------------
  Scenarios Selected  : [Count]
  Scenarios Passed    : [Count]
  Scenarios Failed    : [Count]
  Scenarios Skipped   : [Count]
  Total Run Time      : [Seconds]
  Overall Status      : [PASS/FAIL]
--------------------------------------------------
```

### 2. Allure Advanced Reporting
The framework generates a rich, interactive HTML report (`reports/allure-report`):
- **Visual Evidence**: Screenshots are embedded directly inside failed steps.
- **Trends**: Tracks execution history across multiple runs.
- **Categories**: Automatically groups failures into "Assertion Issues", "Timeouts", or "Product Bugs".
- **Environment Details**: Displays OS, Python version, and Browser info.
- **Timeline**: A Gantt-chart style view of scenario durations.

### 3. Failure Forensics
- **Logs**: Detailed tracebacks are saved in `logs/` directory.
- **Screenshots**: High-resolution PNGs are saved in `screenshots/` with timestamps for easy debugging.

---

## 🛠️ How to Run
1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
2. **Execute Tests**:
   - Run everything: `behave`
   - Run with Reporting: `run_allure_report.bat`
   - Run specific feature: `behave features/login.feature`
