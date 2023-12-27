import sys
from typing import List
from sample_ml.logger import logging
from sample_ml.exception import SampleMLException
from sample_ml.entity.config_entity import ModelTrainerConfig
from sample_ml.entity.artifact_entity import ModelTrainerArtifact, DataTransformationArtifact
from sample_ml.utils.utility import load_object, save_object
from sample_ml.entity.model_factory import (
    ModelFactory, 
    GridSearchedBestModel, 
    MetricInfoArtifact,
    evaluate_regression_model
)



class HousingEstimatorModel:

    def __init__(self, preprocessor_object: object, trained_model_object: object) -> None:
        """
        TrainedModel constructor
        preprocessing_object: preprocessing_object
        trained_model_object: trained_model_object
        """
        self.preprocessor =preprocessor_object
        self.trained_model = trained_model_object

    def predict(self, X):
        """
        function accepts raw inputs and then transformed raw input using preprocessing_object
        which gurantees that the inputs are in the same format as the training data
        At last it perform prediction on transformed features
        """
        transformed_feature = self.preprocessor.transform(X)
        return self.trained_model.predict(transformed_feature)

    def __repr__(self) -> str:
        return f"{type(self.trained_model).__name__}()"

    def __str__(self) -> str:
        return f"{type(self.trained_model).__name__}()"



class ModelTrainer:

    def __init__(self,
                 model_trainer_config: ModelTrainerConfig, 
                 data_transformation_artifact: DataTransformationArtifact
                 ) -> None:
        
        logging.info(f"{'#'*10} Model Training Started {'#'*10}")
        self.model_trainer_config = model_trainer_config
        self.data_transformation_artifact = data_transformation_artifact


    

    def initiate_model_trainer(self):
        try:
            logging.info('Loading Transformed Training Data')
            transformed_train_data_path = self.data_transformation_artifact.transformed_train_path
            train_array = load_object(transformed_train_data_path)
            
            logging.info('Loading Transformed Testing Data')
            transformed_test_data_path = self.data_transformation_artifact.transformed_test_path
            test_array = load_object(transformed_test_data_path)

            logging.info('Splitting Transformed Data into Input and Target feature')
            X_train, y_train = train_array[:, :-1], train_array[:, -1]
            X_test, y_test = test_array[:, :-1], test_array[:, -1]

            model_config_file_path = self.model_trainer_config.model_config_file_path

            logging.info('Initializig Model Factory Class')
            model_factory = ModelFactory(model_config_file_path)

            base_accuracy = self.model_trainer_config.base_accuracy

            logging.info('Initializing Best Model Operation')
            best_model = model_factory.get_best_model(X=X_train, y=y_train, base_accuracy=base_accuracy)
            
            logging.info(f'Best Model found on training dataset: {best_model}')
            
            logging.info('Extracting Tranined Model list')
            grid_search_best_model_list: List[GridSearchedBestModel] = model_factory.grid_searched_best_model_list

            model_list = [model.best_model for model in grid_search_best_model_list]
            logging.info('Evaluation all trained model on training and testing dataset')

            metric_info: MetricInfoArtifact = evaluate_regression_model(
                model_list=model_list,
                X_train=X_train,
                y_train=y_train,
                X_test=X_test,
                y_test=y_test,
                base_accuracy=base_accuracy
            )
            logging.info('Best Model Found on training and testing dataset')

            preprocessor = load_object(
                filepath=self.data_transformation_artifact.preprocessor_object_file_path
            )
            model_object = metric_info.model_object

            trained_model_file_path = self.model_trainer_config.trained_model_file_path
            housing_model = HousingEstimatorModel(preprocessor_object=preprocessor, trained_model_object=model_object)

            logging.info(f"Saving Model at '{trained_model_file_path}'")
            save_object(
                filepath=trained_model_file_path,
                object=housing_model
            )

            model_trainer_artifact = ModelTrainerArtifact(
                trained_model_file_path=trained_model_file_path,
                train_rmse=metric_info.train_rmse,
                test_rmse=metric_info.test_rmse,
                train_accuracy=metric_info.train_accuracy,
                test_accuracy=metric_info.test_accuracy,
                model_accuracy=metric_info.model_accuracy,
                is_model_trained=True,
                message='Model Trained Successfully'
            )

            logging.info(f'Model Trainig Artifact: {model_trainer_artifact}')
            return model_trainer_artifact






        except Exception as e:
            raise SampleMLException(e, sys) from e

    def __del__(self):
        logging.info(f"{'#'*10} Model Trainer Log complete {'#'*10}")



#############################
# WORKING 
# Loading Transformed training and testing dataset
# Reading Model Config file
# getting best model on training datset
# evaludation models on both training & testing datset -->model object
# loading preprocessing object
# custom model object by combining both preprocessing obj and model obj
# saving custom model object
# return model_trainer_artifact