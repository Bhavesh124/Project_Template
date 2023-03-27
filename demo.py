from Visa_Project.entity.config_entity import DataIngestionConfig
from Visa_Project.entity.artifact_entity import DataIngestionArtifact
from Visa_Project.config.configuration import Configuration
import os,sys
from Visa_Project.logger import logging
from Visa_Project.pipeline.pipeline import Pipeline
from Visa_Project.exception import CustomException

def main():
    try:
        pipeline = Pipeline()
        pipeline.run_pipeline()

    except Exception as e:
        logging.error(f"{e}")
        print(e)

if __name__ == "__main__":
    main()