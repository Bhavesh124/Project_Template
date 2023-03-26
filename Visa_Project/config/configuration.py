import sys
from Visa_Project import *
from Visa_Project import logging
from Visa_Project.exception import CustomException
from Visa_Project.entity.config_entity import *
from Visa_Project.utils.utils import read_yaml_file
from Visa_Project.constant import *

class Configuration:
    def __init__(self,
                 config_file_path:str =CONFIG_FILE_PATH,
                 current_time_stamp:str = CURRENT_TIME_STAMP) -> None:
        try:
            self.config_info = read_yaml_file(file_path=config_file_path)
            self.training_pipeline_config = self.get_training_pipeline_config()
            self.time_stamp = current_time_stamp

        except Exception as e:
            raise CustomException(e,sys) from e
