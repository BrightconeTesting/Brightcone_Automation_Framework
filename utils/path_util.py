import os
from utils.logger_config import logger

class PathUtil:
    """
    Utility class for handling dynamic project paths cross-platform.
    """

    @staticmethod
    def get_project_root():
        """
        Derives the project root directory from the location of this file.
        Assumes this file is in 'utils/path_util.py'.
        """
        # This file is in {root}/utils/path_util.py -> parent of parent is root
        return os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

    @staticmethod
    def get_testdata_dir():
        """Returns the absolute path to the 'testdata' directory."""
        return os.path.join(PathUtil.get_project_root(), "testdata")

    @staticmethod
    def get_test_file(file_name):
        """
        Returns the absolute path to a document in 'testdata/files/'.
        Raises FileNotFoundError if the file does not exist.
        """
        path = os.path.join(PathUtil.get_testdata_dir(), "files", file_name)
        if not os.path.exists(path):
            error_msg = f"Test file not found at: {path}"
            logger.error(error_msg)
            raise FileNotFoundError(error_msg)
        
        logger.info(f"Resolved test file path: {path}")
        return path

    @staticmethod
    def get_excel_file(file_name):
        """
        Returns the absolute path to an Excel file in 'testdata/excel/'.
        Raises FileNotFoundError if the file does not exist.
        """
        path = os.path.join(PathUtil.get_testdata_dir(), "excel", file_name)
        if not os.path.exists(path):
            error_msg = f"Excel file not found at: {path}"
            logger.error(error_msg)
            raise FileNotFoundError(error_msg)
        
        logger.info(f"Resolved Excel file path: {path}")
        return path

    @staticmethod
    def get_config_file(file_name="test_config.json"):
        """Returns the absolute path to a config file in project root or testdata."""
        # Config usually sits directly in testdata or project root. 
        # User requirement says testdata/excel and testdata/files, 
        # let's assume config is in testdata/
        path = os.path.join(PathUtil.get_testdata_dir(), file_name)
        if not os.path.exists(path):
            # Fallback to testdata/excel/ if not in root of testdata
            alt_path = os.path.join(PathUtil.get_testdata_dir(), "excel", file_name)
            if os.path.exists(alt_path):
                return alt_path
            raise FileNotFoundError(f"Config file not found: {file_name}")
        return path
