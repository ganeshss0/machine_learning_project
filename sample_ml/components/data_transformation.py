import os, sys
from sample_ml.logger import logging
from sample_ml.exception import SampleMLException
from sample_ml.entity.config_entity import DataTransformationConfig
from sample_ml.entity.artifact_entity import (
    DataTransformationArtifact, 
    DataIngestionArtifact, 
    DataValidationArtifact
)
from sample_ml.constants import (
    COLUMN_TOTAL_ROOMS,
    COLUMN_POPULATION,
    COLUMN_HOUSEHOLDS,
    COLUMN_TOTAL_BEDROOM,
    SCHEMA_COLUMNS_KEY,
    SCHEMA_CATEGORICAL_COLUMNS_KEY,
    SCHEMA_NUMERICAL_COLUMNS_KEY,
    SCHEMA_TARGET_COLUMN_KEY
    
)
from sample_ml.utils.utility import get_dataset, read_yaml, save_object
import numpy as np
import pandas as pd
from sklearn.pipeline import Pipeline
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder, StandardScaler





class FeatureGenerator(BaseEstimator, TransformerMixin):
    '''
    Class for generating features in datasets.
    * `columns` : Name of columns
    * `add_bedrooms_per_rooms` : Add `bedroom_per_room` column to datasets if `True` else not
    * 
    '''
    def __init__(self,
                 columns: pd.Index = None,
                 add_bedrooms_per_rooms: bool = True,
                 total_bedrooms_idx: int = 3,
                 total_rooms_idx: int = 4,
                 population_idx: int = 5,
                 households_idx: int=6
                 ):
        
        self.add_bedrooms_per_rooms = add_bedrooms_per_rooms
        self.columns = columns
        
        if self.columns is not None:
            total_bedrooms_idx = self.columns.get_loc(COLUMN_TOTAL_BEDROOM)
            total_rooms_idx = self.columns.get_loc(COLUMN_TOTAL_ROOMS)
            population_idx = self.columns.get_loc(COLUMN_POPULATION)
            households_idx = self.columns.get_loc(COLUMN_HOUSEHOLDS)
        
        self.total_bedrooms_idx = total_bedrooms_idx
        self.total_rooms_idx = total_rooms_idx
        self.population_idx = population_idx
        self.households_idx = households_idx


    def fit(self, X):
        return self

    def transform(self, X: np.ndarray) -> np.ndarray:
        
        X = np.array(X)
        room_per_household = X[:, self.total_rooms_idx] / X[:, self.households_idx]
        
        population_per_household = X[:, self.population_idx] / X[:, self.households_idx]
        
        if self.add_bedrooms_per_rooms:
        
            bedrooms_per_rooms = X[:, self.total_bedrooms_idx] / X[:, self.total_rooms_idx]
        
            generated_feature = np.c_[X, room_per_household, population_per_household, bedrooms_per_rooms]
        else:
        
            generated_feature = np.c_[X, room_per_household, population_per_household]
        
        
        self.added_columns = pd.Index(['room_per_household', 'population_per_household', 'bedroom_per_room'])

        

        return generated_feature





class DataTransformation:
    def __init__(self, 
                 data_transformation_config: DataTransformationConfig,
                 data_ingestion_artifact: DataIngestionArtifact, 
                 data_validation_artifact: DataValidationArtifact
                 ) -> None:
        try:
            logging.info(f'{"="*10} Data Transformation Log Start {"="*10}')
            self.data_ingestion_artifact = data_ingestion_artifact
            self.data_validation_artifact = data_validation_artifact
            self.data_transformation_config = data_transformation_config

            self.schema = read_yaml(data_validation_artifact.schema_file_path)
        except Exception as e:
            raise SampleMLException(e, sys)

    def get_data_transformer_object(self) -> ColumnTransformer:
        try:
            logging.info('Reading Schema File')
            
            categorical_columns = self.schema[SCHEMA_CATEGORICAL_COLUMNS_KEY]
            numerical_columns = self.schema[SCHEMA_NUMERICAL_COLUMNS_KEY]
            
            logging.info('Creating Numerical Pipeline')
            numerical_pipeline = Pipeline(steps=[
                ('imputer', SimpleImputer(strategy='median')),
                ('feature-generator', FeatureGenerator(
                    add_bedrooms_per_rooms=self.data_transformation_config.add_bedroom_per_room
                )),
                ('scaler', StandardScaler())
            ])
            logging.info(f'Numerical Pipeline Created {numerical_pipeline}')

            logging.info('Creating Categorical Pipeline')
            categorical_pipeline = Pipeline(steps=[
                ('impute', SimpleImputer(strategy='most_frequent')),
                ('one-hot-encoder', OneHotEncoder())
            ])
            logging.info(f'Categorical Pipeline Created: {categorical_pipeline}')


            preprocessor = ColumnTransformer(transformers=[
                ('numerical-pipeline', numerical_pipeline, numerical_columns),
                ('categorical-pipeline', categorical_pipeline, categorical_columns)
            ])

            return preprocessor
        except Exception as e:
            raise SampleMLException(e, sys)
    
    def load_datasets(self):
 
        train_data = get_dataset(
            file_path=self.data_ingestion_artifact.train_data_path,
            schema=self.schema
        )
        test_data = get_dataset(
            file_path=self.data_ingestion_artifact.test_data_path,
            schema=self.schema
        )
        return train_data, test_data
    

    def initiate_data_transformation(self) -> DataTransformationArtifact:
        try:
            logging.info('Loading Preprocessor Object')
            preprocessor = self.get_data_transformer_object()
            
            logging.info('Loading Train Test Datasets')
            train_data, test_data = self.load_datasets()

            target_column_name = self.schema[SCHEMA_TARGET_COLUMN_KEY]

            logging.info('Splitting Dependent and Independent Features in datasets')
            input_train_feature_data = train_data.drop(columns=[target_column_name])
            
            target_train_data = train_data[target_column_name]
            input_test_feature_data = test_data.drop(columns=[target_column_name])
            
            target_test_data = test_data[target_column_name]
            
            logging.info('Transforming Train and Test Data')
            input_train_feature_array = preprocessor.fit_transform(input_train_feature_data)
            input_test_feature_array = preprocessor.transform(input_test_feature_data)

            train_array = np.c_[input_train_feature_array, np.array(target_train_data)]
            test_array = np.c_[input_test_feature_array, np.array(target_test_data)]


            train_data_file_name = os.path.basename(self.data_ingestion_artifact.train_data_path).replace('.csv', '.npy')
            test_data_file_name = os.path.basename(self.data_ingestion_artifact.test_data_path).replace('csv', '.npy')

            transformaed_train_data_file = os.path.join(
                self.data_transformation_config.transformed_train_dir, 
                train_data_file_name
            )
            transformaed_test_data_file = os.path.join(
                self.data_transformation_config.transformed_test_dir,
                test_data_file_name
            )

            logging.info('Saving Transformed Data into Numpy Binary')
            save_object(
                filepath=transformaed_train_data_file,
                object=train_array
            )
            save_object(
                filepath=transformaed_test_data_file,
                object=test_array
            )
            logging.info('Saving Preprocessor Object')
            save_object(
                filepath=self.data_transformation_config.preprocessed_object_file_path,
                object=preprocessor
            )
            
            data_transformation_artifact = DataTransformationArtifact(
                transformed_train_path=transformaed_train_data_file,
                transformed_test_path=transformaed_test_data_file,
                preprocessor_object_file_path=self.data_transformation_config.preprocessed_object_file_path,
                message='Data Transformation Successfull.',
                is_transformed=True
            )

            logging.info(f'Data Transformation Successfull: {data_transformation_artifact}')

            return data_transformation_artifact
            


        
        except Exception as e:
            raise SampleMLException(e, sys)

    
    def __del__(self):
        logging.info(f'{"="*10} Data Transformation Log Complete {"="*10}')
    