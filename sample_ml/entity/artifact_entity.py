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
        'k'
    ]
)

DataTransformationArtifact = namedtuple(
    'DataTransformationArtifact',
    [
        'k'
    ]
)