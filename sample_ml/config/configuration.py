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
            data_ingestion_artifact_dir = os.path.join(
                self.training_pipeline_config.artifact_dir,
                DATA_INGESTION_ARTIFACT_DIR,
                self.time_stamp
            )
            
            logging.info('Creating Download File Path')
            tgz_data_dir = os.path.join(
                data_ingestion_artifact_dir,
                data_ingestion_config[DATA_INGESTION_TGZ_DOWNLOAD_DIR_KEY]
            )
            
            logging.info('Creating Extracted File Path')
            raw_data_dir = os.path.join(
                data_ingestion_artifact_dir,
                data_ingestion_config[DATA_INGESTION_RAW_DATA_DIR_KEY]
            )
            
            logging.info('Creating Ingested Data Path for Train and Test Files')
            ingested_data_dir = os.path.join(
                data_ingestion_artifact_dir,
                data_ingestion_config[INGESTION_DATA_DIR_KEY]
            )
            
            logging.info('Creating Train File Path')
            train_data_dir = os.path.join(
                ingested_data_dir,
                data_ingestion_config[DATA_INGESTION_TRAIN_DIR_KEY]
            )
            
            logging.info('Creating Test File Path')
            test_data_dir = os.path.join(
                ingested_data_dir,
                data_ingestion_config[DATA_INGESTION_TEST_DIR_KEY]
            )
            
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
        try:
            data_transformation_config = self.config_info[DATA_TRANSFORMATION_CONFIG_KEY]

            data_transformation_artifact_dir = os.path.join(
                self.training_pipeline_config.artifact_dir,
                DATA_TRANSFORMATION_ARTIFACT_KEY,
                self.time_stamp
            )
            
            add_bedroom_per_room = data_transformation_config[DATA_TRANSFORMATION_ADD_BEDROOM_PER_ROOM_KEY]

            transformed_test_dir = os.path.join(
                data_transformation_artifact_dir,
                data_transformation_config[DATA_TRANSFORMATION_TRANSFORMED_DIR_KEY],
                data_transformation_config[DATA_TRANSFORMATION_TRANSFORMED_TEST_DIR_KEY]
            )

            transformed_train_dir = os.path.join(
                data_transformation_artifact_dir,
                data_transformation_config[DATA_TRANSFORMATION_TRANSFORMED_DIR_KEY],
                data_transformation_config[DATA_TRANSFORMATION_TRANSFORMED_TRAIN_DIR_KEY]
            )

            preprocessor_object_file_path = os.path.join(
                data_transformation_artifact_dir,
                data_transformation_config[DATA_TRANSFORMATION_PREPROCESSOR_DIR_KEY],
                data_transformation_config[DATA_TRANSFORMATION_PREPROCESSOR_FILE_KEY]
            )

            logging.info('Data Transformation Config')
            return DataTransformationConfig(
                add_bedroom_per_room=add_bedroom_per_room,
                transformed_train_dir=transformed_train_dir,
                transformed_test_dir=transformed_test_dir,
                preprocessed_object_file_path=preprocessor_object_file_path
            )
        
        except Exception as e:
            raise SampleMLException(e, sys)


    def get_data_validation_config(self) -> DataValidationConfig:
        try:
            data_validation_config = self.config_info[DATA_VALIDATION_CONFIG_KEY]

            data_validation_artifact_dir = os.path.join(
                self.training_pipeline_config.artifact_dir,
                DATA_VALIDATION_ARTIFACT_DIR,
                self.time_stamp
            )
            
            schema_file = os.path.join(
                ROOT_DIR, 
                data_validation_config[DATA_VALIDATION_SCHEMA_DIR_KEY], 
                data_validation_config[DATA_VALIDATION_SCHEMA_FILE_KEY]
            )

            report_file = os.path.join(
                data_validation_artifact_dir, 
                data_validation_config[DATA_VALIDATION_REPORT_FILE_KEY]
            )

            report_page_file = os.path.join(
                data_validation_artifact_dir, 
                data_validation_config[DATA_VALIDATION_REPORT_PAGE_FILE_KEY]
            )


            return DataValidationConfig(
                schema_file_path=schema_file,
                report_file_path=report_file,
                report_page_file_path=report_page_file
            )
        except Exception as e:
            raise SampleMLException(e, sys) from e


    def get_model_trainer_config(self) -> ModelTrainerConfig:
        try:
            # Artifact Directory
            artifact_dir = self.training_pipeline_config.artifact_dir
            
            model_trainer_artifact_dir = os.path.join(
                artifact_dir,
                MODEL_TRAINER_ARTIFACT_KEY,
                self.time_stamp
            )
            model_trainer_config = self.config_info[MODEL_TRAINER_CONFIG_KEY]
            
            # Base Accuracy of the Model
            base_accuracy = model_trainer_config[MODEL_TRAINER_BASE_ACCURACY_KEY]

            model_config_file_path = os.path.join(
                ROOT_DIR,
                model_trainer_config[MODEL_TRAINER_MODEL_CONFIG_DIR_KEY],
                model_trainer_config[MODEL_TRAINER_MODEL_CONFIG_FILE_KEY]
            )

            trained_model_file_path = os.path.join(
                model_trainer_artifact_dir,
                model_trainer_config[MODEL_TRAINER_TRAINED_MODEL_DIR_KEY],
                model_trainer_config[MODEL_TRAINER_MODEL_FILE_KEY]
            )

            model_trainer_config = ModelTrainerConfig(
                model_config_file_path=model_config_file_path,
                trained_model_file_path=trained_model_file_path,
                base_accuracy=base_accuracy
            )

            logging.info(f"Model Trainer Config: {model_trainer_config}")

            return model_trainer_config

        except Exception as e:
            logging.error(e.__str__())
            raise SampleMLException(e, sys) from e


    def get_model_evaluation_config(self) -> ModelEvaluationConfig:
        try:
            model_evaluation_config = self.config_info[MODEL_EVALUATION_CONFIG_KEY]

            artifact_dir = self.training_pipeline_config.artifact_dir

            model_evaluation_artifact_dir = os.path.join(
                artifact_dir,
                MODEL_EVALUATION_ARTIFACT_KEY,
                self.time_stamp
            )
            model_evaluation_file_name = os.path.join(
                model_evaluation_artifact_dir,
                model_evaluation_config[MODEL_EVALUATION_FILE_KEY]
            )
            model_evaluation_config = ModelEvaluationConfig(
                model_evaluation_file=model_evaluation_file_name,
                time_stamp=self.time_stamp
            )
            logging.info(f'Model Evaluation Config: {model_evaluation_config}')
            return model_evaluation_config
        except Exception as e:
            logging.error(e.__str__())
            raise SampleMLException(e, sys)

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
        
    
