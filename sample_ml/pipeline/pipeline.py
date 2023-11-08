import os, sys
from sample_ml.config.configuration import Configuration
from sample_ml.logger import logging
from sample_ml.exception import SampleMLException

from sample_ml.entity.artifact_entity import *
from sample_ml.entity.config_entity import DataIngestionConfig
from sample_ml.components.data_ingestion import DataIngestion



class Pipeline:

    def __init__(self, config: Configuration=Configuration) -> None:
        try:
            self.config = config()
        except Exception as e:
            raise SampleMLException(e, sys) from e

    def start_data_ingestion(self) -> DataIngestionArtifact:
        try:
            logging.info('Starting Data Ingestion Pipeline')
            data_ingestion = DataIngestion(
                data_ingestion_config=self.config.get_data_ingestion_config()
            )
            logging.info('Data Ingestion Pipeline Sucessful')
            return data_ingestion.initiate_data_ingestion()
        except Exception as e:
            logging.error(f'Data Ingestion Pipeline Failed: {e}')
            raise SampleMLException(e, sys) from e
    
    def start_data_validation(self) -> DataValidationArtifact:
        pass

    def start_data_transformation(self) -> DataTransformationArtifact:
        pass

    def start_model_trainer(self):
        pass

    def run_pipeline(self):
        try:
            data_ingestion_artifact = self.start_data_ingestion()

        except Exception as e:
            raise SampleMLException(e, sys) from e