import os, sys
from sample_ml.logger import logging
from sample_ml.exception import SampleMLException
from sample_ml.entity.config_entity import DataValidationConfig
from sample_ml.entity.artifact_entity import DataIngestionArtifact, DataValidationArtifact
from sample_ml.utils.utility import read_yaml
import pandas as pd
import json

from evidently.model_profile import Profile
from evidently.model_profile.sections import DataDriftProfileSection
from evidently.dashboard import Dashboard
from evidently.dashboard.tabs import DataDriftTab



class DataValidation:
    '''Main Data Validation Class'''

    def __init__(self, data_validation_config: DataValidationConfig, data_ingestion_artifact: DataIngestionArtifact) -> None:
        try:
            # logging.info()
            self.data_validation_config = data_validation_config
            self.data_ingestion_artifact = data_ingestion_artifact
        except Exception as e:
            raise SampleMLException(e, sys) from e



    def is_train_test_file_exists(self) -> bool:
        '''Validate Train and Test datasets exists or not.'''

        logging.info('Checking Train and Test data files')
        train_data_path = self.data_ingestion_artifact.train_data_path
        test_data_path = self.data_ingestion_artifact.test_data_path

        is_train_file_exists = os.path.exists(train_data_path)
        is_test_file_exists = os.path.exists(test_data_path)

        def log_message(file_info, file_path, is_exists):
            '''Simple message logging function.'''

            message = '{} File {} at {}'
            if is_exists:
                logging.info(message.format(file_info, 'Exists', file_path))
            else:
                logging.info(message.format(file_info, 'Not Exists', file_path))

        log_message('Training', train_data_path, is_train_file_exists)
        log_message('Testing', test_data_path, is_test_file_exists)

        
        if not (is_train_file_exists and is_test_file_exists):
            raise FileNotFoundError(f'Training Data File: {train_data_path} or Testing Data File: {test_data_path} is missing')



    def validate_dataset_schema(self) -> bool:
        try:
            
            # assignment validate training and testing dataset using schema file
            # num of columns
            # names of columns
            # check the value of ocean proximity


            train_data_path = self.data_ingestion_artifact.train_data_path
            train_df = pd.read_csv(train_data_path)

            schema_path = self.data_validation_config.schema_file_path
            schema = read_yaml(file_path=schema_path)

            logging.info('Checking Columns in dataframe...')
            schema_columns_dtype = schema['columns']
            dataframe_columns = set(train_df.columns.str.lower())
            schema_cols = set(map(str.lower, schema_columns_dtype))

            # checking columns
            
            if dataframe_columns == schema_cols:
                logging.info('All columns matched')
                logging.info('Checking values in ocean proximity...')

                schema_ocean_proximity_value = set(schema['domain_value']['ocean_proximity'])

                data_ocean_proximity_value = set(train_df['ocean_proximity'].unique())

                if schema_ocean_proximity_value == data_ocean_proximity_value:
                    logging.info('ocean_proximity values matched')   
                else:
                    missing_value = schema_ocean_proximity_value - data_ocean_proximity_value
                    extra_value = data_ocean_proximity_value - schema_ocean_proximity_value
                    message = f'Missing ocean_proximity values: {missing_value} | Extra ocean_proximity values: {extra_value}'
                    logging.warning(message)
                    raise ValueError(message)
            else:
                missing_cols = schema_cols - dataframe_columns
                extra_cols = dataframe_columns - schema_cols
                message = f'Missing Columns: {missing_cols} | Extra Columns: {extra_cols}'
                logging.warning(message)
                raise ValueError(message)
        

        except Exception as e:
            raise SampleMLException(e, sys) from e
        


    def is_data_drift_found(self) -> bool:
        try:
            report = self.get_and_save_data_drift_report()
            self.save_data_drift_report_page()

            return True
        except Exception as e:
            raise SampleMLException(e, sys) from e



    def get_and_save_data_drift_report(self):
        try:
            profile = Profile(
                sections=[DataDriftProfileSection()]
            )

            train_data, test_data = self.get_train_test_dataframe()
            logging.info('Calculating Data Drift')
            profile.calculate(
                reference_data=train_data,
                current_data=test_data
            )

            report = json.loads(profile.json())
            
            report_file_path = self.data_validation_config.report_file_path
            logging.info(f'Report File saved at {report_file_path}')

            report_dir = os.path.dirname(report_file_path)
            os.makedirs(report_dir, exist_ok=True)
            
            with open(report_file_path, mode='w', encoding='utf-8') as file:
                json.dump(obj=report, fp=file, indent=4)

            return report

        except Exception as e:
            raise SampleMLException(e, sys) from e
        


    def save_data_drift_report_page(self):
        try:
            dashboard = Dashboard(tabs=[DataDriftTab()])
            train_df, test_df = self.get_train_test_dataframe()
            dashboard.calculate(train_df, test_df)
            logging.info(f'Data Drift Page file saved at {self.data_validation_config.report_page_file_path}')
            dashboard.save(filename=self.data_validation_config.report_page_file_path)

        except Exception as e:
            raise SampleMLException(e, sys) from e
    


    def get_train_test_dataframe(self):
        train_data = pd.read_csv(self.data_ingestion_artifact.train_data_path)
        test_data = pd.read_csv(self.data_ingestion_artifact.test_data_path)
        return train_data, test_data



    def initiate_data_validation(self):
        try:
            self.is_train_test_file_exists()
            self.validate_dataset_schema()
            self.is_data_drift_found()
            return DataValidationArtifact(
                schema_file_path=self.data_validation_config.schema_file_path,
                report_file_path=self.data_validation_config.report_file_path,
                report_page_file_path=self.data_validation_config.report_page_file_path,
                message='Data Validation Complete Successful',
                is_validated=True
            )
            
        except Exception as e:
            raise SampleMLException(e, sys) from e
