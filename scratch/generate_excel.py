import openpyxl
import os

def create_sample_excel():
    path = "test_data/test_data_excel.xlsx"
    if not os.path.exists("test_data"):
        os.makedirs("test_data")
        
    wb = openpyxl.Workbook()
    sheet = wb.active
    sheet.title = "LoginData"
    
    # Headers
    headers = ["test_case_id", "username", "password", "expected_status"]
    sheet.append(headers)
    
    # Data
    data = [
        ["TC01", "admin@brightcone.ai", "admin123", "success"],
        ["TC02", "invalid@brightcone.ai", "wrongpass", "failure"],
        ["TC03", "guest@brightcone.ai", "guest123", "success"]
    ]
    
    for row in data:
        sheet.append(row)
        
    wb.save(path)
    print(f"Sample Excel file created at: {path}")

if __name__ == "__main__":
    create_sample_excel()
