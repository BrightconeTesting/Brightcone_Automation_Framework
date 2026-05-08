# 📊 Reporting & Execution

The **Bright Automation** framework's reporting is optimized for quick feedback and deep analysis.

## 1. Console Reporting (Runtime)
The `environment.py` hook provides a **real-time execution summary dashboard**. 
- After all tests finish, you get a clean table showing:
  - **Scenarios Selected**: Total tests run.
  - **Scenarios Passed/Failed**: Detailed ratio.
  - **Total Run Time**: In seconds.
  - **Overall Status**: PASS or FAIL.

## 2. Allure Report (Dashboard)
The primary reporting engine is **Allure**, which creates a high-quality interactive HTML site.

### To generate the report, run:
```bash
run_allure_report.bat
```

### Key Allure Features:
- **📊 Overview**: Summary donut charts and timeline.
- **🖼️ Failures with Screenshots**: `after_step` hook automatically attaches screenshots to the exact failed step.
- **🕝 History & Trends**: Allure stores history in the `reports/` folder. You can see how pass rates change over multiple runs.
- **🛠️ Environment Data**: Shows OS version, Python version, and Browser info.
- **📁 Failure Grouping**: Tests are automatically sorted by category (e.g., "Timeout" or "Product Bug").

## 3. Screenshots (`screenshots/`)
- **Format**: `FAILED_[step_name]_[timestamp].png`
- **Location**: All failure screenshots are stored locally for fast inspection.
- **Quality**: High-resolution PNGs help identify visual bugs.

## 4. Execution Logs (`logs/`)
- A record of every action taken by the framework.
- **Detailed Tracebacks**: When a test fails, the framework logs the exact line of code where it crashed.
- **Visibility**: Level of logs can be adjusted from `INFO` to `DEBUG` for deeper inspection.

---

## 🚀 How to Run the Tests
1. **Full Suite**:
   ```ps1
   behave
   ```
2. **With Allure Reporting**:
   ```ps1
   .\run_allure_report.bat
   ```
3. **Specific Feature**:
   ```ps1
   behave .\features\recruitment.feature
   ```
