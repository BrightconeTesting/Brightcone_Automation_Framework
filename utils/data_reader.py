import json
import os
import openpyxl

class DataReader:
    """
    Utility class to read test data from various formats (JSON, Excel).
    """

    @staticmethod
    def read_json(file_path):
        """
        Reads a JSON file and returns a dictionary.
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"JSON data file not found at: {file_path}")
        
        with open(file_path, 'r') as file:
            return json.load(file)

    @staticmethod
    def read_excel(file_path, sheet_name=None):
        """
        Reads an Excel file and returns data as a list of dictionaries.
        Each dictionary represents a row with headers as keys.
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Excel data file not found at: {file_path}")
        
        workbook = openpyxl.load_workbook(file_path)
        sheet = workbook[sheet_name] if sheet_name else workbook.active
        
        data = []
        headers = [cell.value for cell in sheet[1]]
        
        for row in sheet.iter_rows(min_row=2, values_only=True):
            row_data = dict(zip(headers, row))
            data.append(row_data)
            
        return data

    @staticmethod
    def get_data_by_id(data_list, record_id, id_key='id'):
        """
        Helper to find a specific record in a list of data by its ID.
        """
        for item in data_list:
            if str(item.get(id_key)) == str(record_id):
                return item
        return None
