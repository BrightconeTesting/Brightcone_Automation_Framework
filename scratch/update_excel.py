import openpyxl
import os

file_path = 'test_data/recruitment_data.xlsx'

# Create dir if not exists
os.makedirs('test_data', exist_ok=True)

# Create a new workbook
wb = openpyxl.Workbook()
sheet = wb.active
sheet.title = "Sheet1"

# Headers
headers = ['scenario', 'role', 'file_name', 'expected_result', 'category', 'job_role', 'resume_name']
sheet.append(headers)

# Data
data = [
    # Document scenarios
    ('Upload document and verify its status', 'user', 'Prasaanthi_ML_Resume.pdf', '⚠️ Sensitive information detected. This has been flagged for review.', 'Engineering, Admin, General', '', ''),
    ('Upload and verify admin document', 'user', 'Admin_Policy.pdf', 'uploaded document was uder review', 'Admin', '', ''),
    
    # Login scenario (just to keep it consistent)
    ('Login using email and OTP', 'user', '', 'success', '', '', ''),
    ('Login using email and OTP', 'admin', '', 'success', '', '', ''),
    
    # Recruitment scenarios
    ('Add a resume for ML Engineer role', 'user', 'Munjala_Anand_Tester_Resume (1).docx', 'success', '', 'ML Engineer', ''),
    ('Upload resume with unsupported file format', 'user', 'Basic Java Concepts questions.txt', 'Some files were skipped. Only PDF and DOCX files are supported.', '', 'ML Engineer', ''),
    ('Delete candidate from Recruitment module using dynamic resume name', 'user', '', 'success', '', 'ML Engineer', 'John'),
    ('Validate Approve Shortlist button behavior and navigation to Interview Management', 'user', '', 'User', '', 'QA Engineer', '')
]

for row in data:
    sheet.append(row)

# Save the workbook
wb.save(file_path)
print(f"Successfully updated {file_path}")
