import yaml,sys
import numpy as np
import os,sys
import dill
import pandas as pd
from Visa_Project.constant import *
from Visa_Project.exception import CustomException

def write_yaml_file(file_path:str,data:dict=None):
    """
    create yaml file
    file_path: str
    data: dict
    """

    try:
        os.makedirs(os.path.dirname(file_path),exist_ok=True)
        with open(file_path,"w") as yaml_file:
            if data is not None:
                yaml.dump(data,yaml_file)

    except Exception as e:
        raise CustomException(e,sys)
    
def read_yaml_file(file_pat:str)->dict:
        """
        Reads a yaml file and returns the contents as a dictionary
        file_path: str
        """
        try:
            with open(file_path, 'rb') as yaml_file:
                return yaml.safe_load(yaml_file)
            
        except Exception as e:
            raise CustomException(e,sys) from e