from Visa_Project.pipeline.pipeline import Pipeline
from Visa_Project.exception import CustomException
from Visa_Project.logger import logging
from Visa_Project.config.configuration import Configuration
from Visa_Project.utils.utils import read_yaml_file
import pandas as pd
import collections
import sys

class IngestedDataValidation:

    def __init__(self,validatee_path,schema_path):
        try:
            self.validate_path = validatee_path
            self.schema_path = schema_path
            self.data = read_yaml_file(self.schema_path)

        except Exception as e:
            raise CustomException(e,sys) from e
        
    def validate_file(self, file_name)->bool:
        try:
            print(self.data['Filename'])
            schema_file_name = self.data['Filename']
            if schema_file_name == file_name:
                return True
            
        except Exception as e:
            raise CustomException(e,sys) from e

    def validate_column_length(self)-> bool:
        try:
            df = pd.read_csv(self.validate_path)
            if(df.shape[1] == self.data['NumberofColumns']):
                return True
        except Exception as e:
            raise CustomException(e,sys) from e

    def missing_values_columns(self):
        try:
            df = pd.read_csv(self.validate_path)
            count =0
            for columns in df:
                if (len(df[columns]) - df[columns].count) == len(df[columns]):
                    count+=1
                return True if (count == 0) else False
        except Exception as e:
            raise CustomException(e,sys) from e
        
    def replace_null_values_with_null(self):
        try:
            df = pd.read_csv(self.validate_path)
            df.fillna('NULL',inplace=True)
        except Exception as e:
            raise CustomException(e,sys) from e
        
    def check_columns_name(self)->bool:
        try:
            df = pd.read_csv(self.validate_path)
            df_columns_names = df.columns
            schema_columns_names = list(self.data['ColumnsNames'].keys())

            return True if (collections.Counter(df_columns_names) == collections.Counter(schema_columns_names)) else False
        except Exception as e:
            raise CustomException(e,sys) from e