import openpyxl
import os

def create_recruitment_excel():
    directory = "test_data"
    path = os.path.join(directory, "test_data_excel.xlsx")
    
    if not os.path.exists(directory):
        os.makedirs(directory)
        
    wb = openpyxl.Workbook()
    sheet = wb.active
    sheet.title = "RecruitmentData"
    
    # Headers
    headers = ["scenario", "role", "file_name", "expected_result", "category"]
    sheet.append(headers)
    
    # Sample data matching the requirement: Filter by scenario AND role
    data = [
        ["Upload and verify engineer resume", "user", "Engineer_Resume.pdf", "uploaded document was uder review", "Engineering,Admin,General"],
        ["Upload and verify admin document", "user", "Admin_Policy.pdf", "uploaded document was uder review", "Admin"],
        ["Upload and verify super admin document", "super_admin", "Global_Strategy.pdf", "uploaded document was uder review", "Global"],
        ["Verify document visibility", "user", "User_Manual.pdf", "Success", "Support"]
    ]
    
    for row in data:
        sheet.append(row)
        
    wb.save(path)
    print(f"Refined Excel file created at: {path}")

if __name__ == "__main__":
    create_recruitment_excel()
