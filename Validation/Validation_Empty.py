import pandas as pd

class ValidationFileEmpty:
    def __init__(self, file_Validation):
        self.file_Validation = file_Validation

    def validate_File_empty(self) -> str:
        try:
            # Read File
            df = pd.read_csv(self.file_Validation, sep=',', encoding='latin1')

            # Size file
            size_file = len(df)
            return str(size_file)

        except Exception as e:
            return f"Error: {e}"
