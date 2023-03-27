import sys
from Visa_Project import *
from Visa_Project.logger import logging
from Visa_Project.exception import CustomException
from Visa_Project.entity.config_entity import *
from Visa_Project.utils.utils import read_yaml_file
from Visa_Project.constant import *
from Visa_Project.components.dataingestion import DataIngestion 
from Visa_Project.entity.artifact_entity import DataIngestionArtifact
from Visa_Project.config.configuration import Configuration

class Pipeline():
    def __init__(self, config: Configuration = Configuration()) -> None:
        try:
            self.config = config
        except Exception as e:
            raise CustomException(e,sys)
        
    def start_data_ingestion(self)->DataIngestion:
        try:
            data_ingestion = DataIngestion(data_ingestion_config = self.config.get_data_ingestion_config())
            return data_ingestion.initiate_data_ingestion()
        except Exception as e:
            raise CustomException(e,sys)
        
    def run_pipeline(self):
        try:
            data_ingestion_artifact = self.start_data_ingestion()


        except Exception as e:
            raise CustomException(e,sys)