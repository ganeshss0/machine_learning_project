from yaml import safe_load
from sample_ml.exception import SampleMLException
from sample_ml.logger import logging
import sys



def read_yaml(file_path: str) -> dict:
    '''Reads a YAML file and returns the contents as dictonary object.'''

    try:
        logging.info('Reading Config File')
        with open(file=file_path, mode='r', encoding='utf-8') as file:
            return safe_load(file)
        logging.info('Config File Reading Successfull')
        
    except Exception as e:
        raise SampleMLException(e, sys) from e
