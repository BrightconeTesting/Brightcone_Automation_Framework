# 🏛️ Framework Architecture & Design

The **Bright Automation** framework is built on four core pillars that ensure reliability and scalability.

## 1. Page Object Model (POM)
Separates the **UI Locators** from the **Action Logic**.
- **Pages**: `login_page.py`, `recruitment_page.py`, etc.
- **Benefit**: If a button's ID changes, you only update it in one place (the Page Object), and all tests using that button are automatically fixed.

## 2. Behavior Driven Development (BDD)
Uses **Gherkin** syntax (`Feature`, `Scenario`, `Given`, `When`, `Then`).
- **Features**: Human-readable test cases in `.feature` files.
- **Steps**: Python functions in `steps/` that bridge the gap between English commands and Selenium code.
- **Benefit**: Stakeholders (Product Managers, Devs) can read the tests without knowing Python.

## 3. Environment Hooks (`environment.py`)
Centralized control for test lifecycle.
- **Setup**: `before_all` initializes the Driver Factory and Page Objects.
- **Cleanup**: `after_all` generates final reports and kills the browser.
- **Monitoring**: `after_step` detects failures in real-time.

## 4. WebDriver Factory
Abstracts the browser configuration.
- Supports Chrome via `webdriver-manager`.
- Handles options like window resizing, headless mode, and download paths.
- Ensures consistent browser behavior across different machines.
