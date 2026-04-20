import json
import os
import openpyxl
from utils.logger_config import logger

class DataReader:
    """
    Production-ready utility class to read and filter test data from JSON and Excel.
    """

    @staticmethod
    def read_json(file_path):
        """
        Reads a JSON file and returns a dictionary.
        """
        if not os.path.exists(file_path):
            logger.error(f"JSON data file not found at: {file_path}")
            raise FileNotFoundError(f"JSON data file not found at: {file_path}")
        
        with open(file_path, 'r') as file:
            return json.load(file)

    @staticmethod
    def read_excel_data(file_path, sheet_name=None):
        """
        Reads an Excel file and returns data as a list of dictionaries.
        """
        if not os.path.exists(file_path):
            logger.error(f"Excel data file not found at: {file_path}")
            raise FileNotFoundError(f"Excel data file not found at: {file_path}")
        
        workbook = openpyxl.load_workbook(file_path)
        sheet = workbook[sheet_name] if sheet_name else workbook.active
        
        data = []
        headers = [cell.value for cell in sheet[1]]
        
        for row in sheet.iter_rows(min_row=2, values_only=True):
            if any(row): # Skip empty rows
                row_data = dict(zip(headers, row))
                data.append(row_data)
            
        return data

    @staticmethod
    def get_scenario_data(all_data, scenario_name, role_name):
        """
        Filters data based on scenario name and role.
        """
        logger.debug(f"Filtering data for Scenario: '{scenario_name}' and Role: '{role_name}'")
        
        filtered_data = [
            row for row in all_data 
            if str(row.get('scenario')).strip() == scenario_name.strip() and 
               str(row.get('role')).strip() == role_name.strip()
        ]
        
        if not filtered_data:
            error_msg = f"No test data found for Scenario: '{scenario_name}' with Role: '{role_name}'"
            logger.error(error_msg)
            raise ValueError(error_msg)
        
        return filtered_data[0] # Return the first matching record as a dictionary
