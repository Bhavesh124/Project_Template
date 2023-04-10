import sys,os
from Visa_Project import *
from Visa_Project.logger import logging
from Visa_Project.exception import CustomException
from Visa_Project.entity.config_entity import *
from Visa_Project.utils.utils import read_yaml_file
from Visa_Project.constant import *
from Visa_Project.components.dataingestion import DataIngestion 
from Visa_Project.components.datavalidation import DataValidation
from Visa_Project.components.datatransformation import DataTransformation
from Visa_Project.entity.artifact_entity import DataIngestionArtifact
from Visa_Project.config.configuration import Configuration
from Visa_Project.entity.artifact_entity import DataValidationArtifact,DataTransformationArtifact


class Pipeline():
    def __init__(self, config: Configuration = Configuration()) -> None:
        try:
            self.config = config
        except Exception as e:
            raise CustomException(e,sys)
        
    def start_data_ingestion(self)->DataIngestionArtifact:
        try:
            data_ingestion = DataIngestion(data_ingestion_config = self.config.get_data_ingestion_config()
                                           )
            return data_ingestion.initiate_data_ingestion()
        except Exception as e:
            raise CustomException(e,sys)
        
    def start_data_validation(self,data_ingestion_artifact:DataIngestionArtifact)->DataValidationArtifact:
        try:
            data_validation = DataValidation(data_validation_config = self.config.get_data_validation_config(),
                                             data_ingestion_artifact=data_ingestion_artifact)
            return data_validation.initiate_data_validation()
        except Exception as e:
            raise CustomException(e,sys)
        
    def start_data_transformation(self,data_ingestion_artifact:DataIngestionArtifact,
                                       data_validation_artifact:DataTransformationArtifact)->DataTransformationArtifact:
        try:
            data_transfromation = DataTransformation(
                data_transformation_config=self.config.get_data_transformation_config(),
                data_ingestion_artifact=data_ingestion_artifact,
                data_validation_artifact=data_validation_artifact
            )

            return data_transfromation.initiate_data_transformation()
        except Exception as e:
            raise CustomException(e,sys) from e
        
    def run_pipeline(self):
        try:
            data_ingestion_artifact = self.start_data_ingestion()
            data_validation_artifact = self.start_data_validation(data_ingestion_artifact=data_ingestion_artifact)
            data_transformation_artifact = self.start_data_transformation(data_ingestion_artifact=data_ingestion_artifact,
                                                                          data_validation_artifact=data_validation_artifact)
        except Exception as e:
            raise CustomException(e,sys)