import os, sys
from sample_ml.config.configuration import Configuration
from sample_ml.logger import logging
from sample_ml.exception import SampleMLException

from sample_ml.entity.artifact_entity import *
from sample_ml.entity.config_entity import DataIngestionConfig
from sample_ml.components.data_ingestion import DataIngestion
from sample_ml.components.data_validation import DataValidation



class Pipeline:

    def __init__(self, config: Configuration=Configuration) -> None:
        try:
            self.config = config()
        except Exception as e:
            raise SampleMLException(e, sys) from e

    def start_data_ingestion(self) -> DataIngestionArtifact:
        try:
            logging.info(f'{"#"*5} Data Ingestion Pipeline Start {"#"*5}')
            data_ingestion = DataIngestion(
                data_ingestion_config=self.config.get_data_ingestion_config()
            )
            logging.info(f'{"#"*5} Data Ingestion Pipeline Sucessful {"#"*5}')
            return data_ingestion.initiate_data_ingestion()
        except Exception as e:
            logging.error(f'Data Ingestion Pipeline Failed: {e}')
            raise SampleMLException(e, sys) from e
    
    def start_data_validation(self, data_ingestion_artifact: DataValidationArtifact) -> DataValidationArtifact:
        try:
            logging.info(f'{"#"*5} Data Validation Pipeline Start {"#"*5}')
            data_validation = DataValidation(
                data_validation_config=self.config.get_data_validation_config(),
                data_ingestion_artifact=data_ingestion_artifact
                )
            logging.info(f'{"#"*5} Data Validation Pipeline Successful {"#"*5}')
            return data_validation.initiate_data_validation()
        except Exception as e:
            logging.error(f'Data Validation Pipeline Failed: {e}')

    def start_data_transformation(self) -> DataTransformationArtifact:
        try:
            pass
        except Exception as e:
            logging.error(f'Data Transformation Failed: {e}')

    def start_model_trainer(self):
        pass

    def run_pipeline(self):
        try:
            data_ingestion_artifact = self.start_data_ingestion()
            data_validation_artifact = self.start_data_validation(data_ingestion_artifact)


        except Exception as e:
            raise SampleMLException(e, sys) from e