import json
import os

class FileHandler:
    """Class to handle file operations for Student records."""
    def __init__(self, file_path):
        self.file_path = file_path
        # Ensure directories exist
        dir_name = os.path.dirname(file_path)
        if dir_name and not os.path.exists(dir_name):
            os.makedirs(dir_name)

    def load_data(self):
        """Loads student data from JSON file. Returns a list of dicts."""
        if not os.path.exists(self.file_path):
            # Create an empty file with empty list structure
            self.save_data([])
            return []
        
        try:
            with open(self.file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                if not isinstance(data, list):
                    raise ValueError("JSON root element must be a list.")
                return data
        except json.JSONDecodeError as e:
            raise IOError(f"Data file is corrupted: Invalid JSON format. Details: {e}")
        except PermissionError:
            raise IOError("Permission denied while accessing the data file.")
        except Exception as e:
            raise IOError(f"Error reading data file: {e}")

    def save_data(self, data_list):
        """Saves a list of dictionaries to the JSON file."""
        try:
            with open(self.file_path, "w", encoding="utf-8") as f:
                json.dump(data_list, f, indent=4)
        except PermissionError:
            raise IOError("Permission denied while saving the data file.")
        except Exception as e:
            raise IOError(f"Error writing to data file: {e}")
