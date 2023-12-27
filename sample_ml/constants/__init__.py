import os
from datetime import datetime
import inspect


# ROOT_DIR = os.getcwd()
CURRENT_DIR = os.path.dirname(inspect.getfile(inspect.currentframe()))
ROOT_DIR = os.path.abspath(os.path.join(CURRENT_DIR, os.pardir, os.pardir))
os.chdir(ROOT_DIR)

CONFIG_DIR = 'config'
CONFIG_FILE = 'config.yml'

CONFIG_FILE_PATH = os.path.join(CONFIG_DIR, CONFIG_FILE)

# current_dir = os.path.dirname(inspect.getfile(inspect.currentframe())) 

CURRENT_TIME_STAMP = f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"


# Training pipeline variable
TRAINING_PIPELINE_CONFIG_KEY = 'training_pipeline_config'
# TRAINING_PIPELINE_NAME_KEY = 'pipeline_name'
TRAINING_PIPELINE_ARTIFACT_DIR_KEY = 'artifact_dir'


# Data Ingestion Variable
DATA_INGESTION_CONFIG_KEY = 'data_ingestion_config'
DATA_INGESTION_ARTIFACT_DIR = 'data_ingestion'
DATA_INGESTION_DOWNLOAD_URL_KEY = 'dataset_download_url'
DATA_INGESTION_RAW_DATA_DIR_KEY = 'raw_data_dir'
DATA_INGESTION_TGZ_DOWNLOAD_DIR_KEY = 'tgz_download_dir'
INGESTION_DATA_DIR_KEY = 'ingested_dir'
DATA_INGESTION_TRAIN_DIR_KEY = 'ingested_train_dir'
DATA_INGESTION_TEST_DIR_KEY = 'ingested_test_dir'


# Data Validation Variable
DATA_VALIDATION_CONFIG_KEY = 'data_validation_config'
DATA_VALIDATION_ARTIFACT_DIR = 'data_validation'
DATA_VALIDATION_SCHEMA_DIR_KEY = 'schema_dir'
DATA_VALIDATION_SCHEMA_FILE_KEY = 'schema_file_name'
DATA_VALIDATION_REPORT_FILE_KEY = 'report_file_name'
DATA_VALIDATION_REPORT_PAGE_FILE_KEY = 'report_page_file_name'



# Data Transformation Variable
DATA_TRANSFORMATION_CONFIG_KEY = 'data_transformation_config'
DATA_TRANSFORMATION_ARTIFACT_KEY = 'data_transformation'
DATA_TRANSFORMATION_ADD_BEDROOM_PER_ROOM_KEY = 'add_bedroom_per_room'
DATA_TRANSFORMATION_TRANSFORMED_DIR_KEY = 'transformed_dir'
DATA_TRANSFORMATION_TRANSFORMED_TRAIN_DIR_KEY = 'transformed_train_dir'
DATA_TRANSFORMATION_TRANSFORMED_TEST_DIR_KEY = 'transformed_test_dir'
DATA_TRANSFORMATION_PREPROCESSOR_DIR_KEY = 'preprocessing_dir'
DATA_TRANSFORMATION_PREPROCESSOR_FILE_KEY = 'preprocessor_object_file_name'

# Model Trainer Config
MODEL_TRAINER_CONFIG_KEY = 'model_trainer_config'
MODEL_TRAINER_ARTIFACT_KEY = 'model_trainer'
MODEL_TRAINER_TRAINED_MODEL_DIR_KEY = 'trained_model_dir'
MODEL_TRAINER_MODEL_FILE_KEY = 'model_file_name'
MODEL_TRAINER_BASE_ACCURACY_KEY = 'base_accuracy'
MODEL_TRAINER_MODEL_CONFIG_DIR_KEY = 'model_config_dir'
MODEL_TRAINER_MODEL_CONFIG_FILE_KEY = 'model_config_file_name'

# Model Evaluation Config
MODEL_EVALUATION_CONFIG_KEY = 'model_evaluation_config'
MODEL_EVALUATION_ARTIFACT_KEY = 'model_evaluation'
MODEL_EVALUATION_FILE_KEY = 'model_evaluation_file_name'

# Model Pusher Config
MODEL_PUSHER_CONFIG_KEY = 'model_pusher_config'
MODEL_PUSHER_ARTIFACT_KEY = 'model_pusher'
MODEL_PUSHER_MODEL_EXPORT_DIR = 'model_export_dir'

# Model Evaluation Config
MODEL_EVALUATION_CONFIG_KEY = 'model_evaluation_config'
MODEL_EVALUATION_FILE_NAME_KEY = 'model_evaluation_file_name'
MODEL_EVALUATION_ARTIFACT_KEY = 'model_evaluation'

# Datasets Config
COLUMN_TOTAL_ROOMS = "total_rooms"
COLUMN_POPULATION = "population"
COLUMN_HOUSEHOLDS = "households"
COLUMN_TOTAL_BEDROOM = "total_bedrooms"
COLUMN_OCEAN_PROXIMITY = 'ocean_proximity'

# Schema keys
SCHEMA_COLUMNS_KEY = 'columns'
SCHEMA_NUMERICAL_COLUMNS_KEY = 'numerical_columns'
SCHEMA_CATEGORICAL_COLUMNS_KEY = 'categorical_columns'
SCHEMA_DOMAIN_VALUE_KEY = 'domain_value'
SCHEMA_OCEAN_PROXIMITY_COLUMN_KEY = 'ocean_proximity'
SCHEMA_TARGET_COLUMN_KEY = 'target_column'