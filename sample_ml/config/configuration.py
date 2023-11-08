from sample_ml.entity.config_entity import (
    DataIngestionConfig,
    DataTransformationConfig,
    DataValidationConfig,
    ModelTrainerConfig,
    ModelEvaluationConfig,
    ModelPusherConfig,
    TrainingPipelineConfig
)

from sample_ml.utils.utility import read_yaml
from sample_ml.constants import *
from sample_ml.exception import SampleMLException
import os, sys
from sample_ml.logger import logging





class Configuration:
    '''Base Configuration Class'''

    def __init__(self, config_file_path: str = CONFIG_FILE_PATH) -> None:
        self.config_info = read_yaml(file_path=config_file_path)
        self.training_pipeline_config = self.get_training_pipeline_config()
        self.time_stamp = CURRENT_TIME_STAMP
    

    def get_data_ingestion_config(self) -> DataIngestionConfig:
        try:
            logging.info('Fetching Data Ingestion Config')
            data_ingestion_config = self.config_info[DATA_INGESTION_CONFIG_KEY]
            logging.info('Creating Data Ingestion Artifact Directory Path')
            data_ingestion_artifact_dir = os.path.join(self.training_pipeline_config.artifact_dir,
                DATA_INGESTION_ARTIFACT_DIR,
                self.time_stamp
                )
            
            logging.info('Creating Download File Path')
            tgz_data_dir = os.path.join(data_ingestion_artifact_dir,
                                        data_ingestion_config[DATA_INGESTION_TGZ_DOWNLOAD_DIR_KEY])
            
            logging.info('Creating Extracted File Path')
            raw_data_dir = os.path.join(data_ingestion_artifact_dir,
                                        data_ingestion_config[DATA_INGESTION_RAW_DATA_DIR_KEY])
            
            logging.info('Creating Ingested Data Path for Train and Test Files')
            ingested_data_dir = os.path.join(data_ingestion_artifact_dir,
                                                data_ingestion_config[INGESTION_DATA_DIR_KEY])
            
            logging.info('Creating Train File Path')
            train_data_dir = os.path.join(ingested_data_dir,
                                            data_ingestion_config[DATA_INGESTION_TRAIN_DIR_KEY])
            logging.info('Creating Test File Path')
            test_data_dir = os.path.join(ingested_data_dir,
                                            data_ingestion_config[DATA_INGESTION_TEST_DIR_KEY])
            
            logging.info('Data Ingestion Config')
            return DataIngestionConfig(
                dataset_download_url=data_ingestion_config[DATA_INGESTION_DOWNLOAD_URL_KEY],
                tgz_download_dir=tgz_data_dir,
                raw_data_dir=raw_data_dir,
                ingestion_train_dir=train_data_dir,
                ingested_test_dir=test_data_dir
            )
        except Exception as e:
            
            raise SampleMLException(e, sys) from e

    def get_data_transformation_config(self) -> DataTransformationConfig:
        pass

    def get_data_validation_config(self) -> DataValidationConfig:
        data_validation_config = self.config_info[DATA_VALIDATION_CONFIG_KEY]

        # schme_file = os.path.
        pass

    def get_model_trainer_config(self) -> ModelTrainerConfig:
        model_trainer_config = self.config_info[MODEL_TRAINER_CONFIG_KEY]

    def get_model_evaluation_config(self) -> ModelEvaluationConfig:
        model_evaluation_config = self.config_info[MODEL_EVALUATION_CONFIG_KEY]

    def get_model_pusher_config(self) -> ModelPusherConfig:
        model_pusher_config = self.config_info[MODEL_PUSHER_CONFIG_KEY]
        

    def get_training_pipeline_config(self) -> TrainingPipelineConfig:
        try:
            training_pipeline_config = self.config_info[TRAINING_PIPELINE_CONFIG_KEY]
            artifact_dir = os.path.join(ROOT_DIR, training_pipeline_config[TRAINING_PIPELINE_ARTIFACT_DIR_KEY])
            logging.info('Training Pipeline Config')
            return TrainingPipelineConfig(artifact_dir=artifact_dir)

        except Exception as e:
            raise SampleMLException(e, sys) from e
        
    
