import sys
from sample_ml.exception import SampleMLException
from sample_ml.logger import logging
from sample_ml.entity.config_entity import ModelEvaluationConfig
from sample_ml.entity.artifact_entity import (
    DataIngestionArtifact,
    DataValidationArtifact,
    ModelTrainerArtifact
)


class ModelEvaluation:
    def __init__(self,
                model_evaluation_config: ModelEvaluationConfig,
                data_ingestion_artifact: DataIngestionArtifact,
                data_validation_artifact: DataValidationArtifact,
                model_trainer_artifact: ModelTrainerArtifact
                ) -> None:
        
        try:
            logging.info(f'{"#"*10} Model Evaluation Log Started {"#"*10}')
            self.model_evaluation_config = model_evaluation_config
            self.data_ingestion_artifact = data_ingestion_artifact
            self.data_validation_artifact = data_validation_artifact
            self.model_trainer_artifact = model_trainer_artifact
        except Exception as e:
            logging.error(e.__str__())
            raise SampleMLException(e, sys)

    def get_best_model(self):
        pass

    