# 🧪 Automation Modules & Coverage

The **Bright Automation** framework's current implementation covers three critical user journeys.

## 1. Authentication Module (`login.feature`)
- **Login Flow**: Standard login with email/password.
- **OTP Screen**: Automated 2FA bypass.
- **Verification**: `Then I should be on the dashboard`
- **Error Handling**: Detects and reports invalid credentials.

## 2. Recruitment Module (`recruitment.feature`)
- **Action**: `When I click on Recruitment`
- **Candidate Creation**: `When I add a new candidate`
- **Dashboard View**: Validates if the candidate list is visually updated.
- **Transitions**: Moving candidates between statuses.

## 3. Documents Module (`documents.feature`)
- **Action**: `When I upload a file to Admin category`
- **OS-Interaction**: Uses `PyAutoGUI` to handle Windows "File Open" dialogs.
- **Category Support**: Tests Admin, Engineering, and Support upload zones.
- **Verification**: `Then the file should be successfully uploaded`
- **Reliability**: Uses `pyperclip` system clipboard for 100% path accuracy during paste operations.

---

## 🛠️ Implementation Details
Each module consists of:
1. **Feature File**: The business-level description.
2. **Step Definition**: The technical implementation (Glue).
3. **Page Object**: The UI interaction layer.
