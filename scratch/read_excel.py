import openpyxl
import os

def read_excel():
    file_path = r'c:\Users\Dell\OneDrive\Desktop\Bright_Automation_Before_Adding_Session\testdata\excel\recruitment_data.xlsx'
    
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return

    wb = openpyxl.load_workbook(file_path)
    sheet = wb.active
    
    headers = [cell.value for cell in sheet[1]]
    print(f"Headers: {headers}")
    
    for row_idx, row in enumerate(sheet.iter_rows(min_row=2, values_only=True), start=2):
        if row[0] == "send interview invitation":
             print(f"Row {row_idx}: {dict(zip(headers, row))}")

if __name__ == "__main__":
    read_excel()
