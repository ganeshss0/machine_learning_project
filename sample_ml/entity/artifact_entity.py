from collections import namedtuple


DataIngestionArtifact = namedtuple(
    'DataIngestionArtifact',
    [
        'train_data_path',
        'test_data_path',
        'is_ingested',
        'message'
    ]
)

DataValidationArtifact = namedtuple(
    'DataValidationAritfact',
    [
        'schema_file_path',
        'report_file_path',
        'report_page_file_path',
        'is_validated',
        'message'
    ]
)

DataTransformationArtifact = namedtuple(
    'DataTransformationArtifact',
    [
        'transformed_train_path',
        'transformed_test_path',
        'preprocessor_object_file_path',
        'is_transformed',
        'message'
    ]
)


ModelTrainerArtifact = namedtuple(
    'ModelTrainerArtifact',
    [
        'trained_model_file_path',
        'train_rmse',
        'test_rmse',
        'train_accuracy',
        'test_accuracy',
        'model_accuracy',
        'is_model_trained',
        'message'
    ]
)

ModelEvaluationArtifact = namedtuple(
    'ModelEvaluationArtifact',
    [
        'x'
    ]
)