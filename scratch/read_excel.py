import openpyxl
import os

def read_excel(file_path):
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return
    
    workbook = openpyxl.load_workbook(file_path)
    sheet = workbook.active
    
    print(f"--- Data from {file_path} ---")
    headers = [cell.value for cell in sheet[1]]
    print(f"Headers: {headers}")
    
    for row in sheet.iter_rows(min_row=2, values_only=True):
        if any(row):
            print(row)

read_excel('test_data/recruitment_data.xlsx')
read_excel('test_data/test_data_excel.xlsx')
