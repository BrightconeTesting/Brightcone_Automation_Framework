import openpyxl
import os

def check_excel():
    path = "test_data/test_data_excel.xlsx"
    if not os.path.exists(path):
        print("File does not exist")
        return
        
    wb = openpyxl.load_workbook(path)
    sheet = wb.active
    print(f"Sheet Name: {sheet.title}")
    for row in sheet.iter_rows(values_only=True):
        print(row)

if __name__ == "__main__":
    check_excel()
