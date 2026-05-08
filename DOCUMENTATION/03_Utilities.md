# 🧰 Power Utilities & Helpers

The **Bright Automation** framework's efficiency comes from these behind-the-scenes helpers.

## 1. Gmail OTP Utility (`gmail_util.py`)
Since standard 2FA is a blocker for automation, I integrated an **IMAP-based reader**.
- **Process**:
  1. Requests OTP on the webpage.
  2. Framework waits 3-5 seconds.
  3. `GmailUtil` connects to `munjalaharikrishna123@gmail.com`.
  4. Searches for the latest "OTP" subject.
  5. Extracts the 6-digit code using **Regex**.
  6. Automatically fills it on the UI.
- **Benefit**: No manual intervention is needed for the login process.

## 2. Logger Configuration (`logger_config.py`)
Customized Python `logging` for top-tier visibility.
- **Log Level**: Set to `INFO` for standard runs, `DEBUG` for troubleshooting.
- **Formatting**: Includes `%(asctime)s`, `%(levelname)s`, and `%(message)s`.
- **Visibility**: Logs are printed to the console and saved to the `logs/` directory.

## 3. OS Interop Utility (`pyautogui` & `pyperclip`)
Used to automate the Windows File Explorer.
- **Technique**:
  - `pyperclip.copy(file_path)`: Copies path to the system clipboard.
  - `pyautogui.hotkey('ctrl', 'v')`: Pastes the path into the filename field.
  - `pyautogui.press('enter')`: Confirms the upload.
- **Benefit**: Solves the "Selenium cannot click Windows buttons" problem.

## 4. Requirement Management (`requirements.txt`)
All dependencies are strictly version-controlled to ensure the environment is reproducible.
- Includes `selenium`, `webdriver-manager`, `imap-tools`, `behave`, `allure-behave`, `pyautogui`, `pyperclip`, `python-dotenv`.
