import os, sys
from sample_ml.entity.config_entity import DataIngestionConfig
from sample_ml.exception import SampleMLException
from sample_ml.logger import logging
from sample_ml.entity.artifact_entity import DataIngestionArtifact
import pandas as pd
import numpy as np
from six.moves import urllib
import tarfile
from sklearn.model_selection import StratifiedShuffleSplit

class DataIngestion:

    def __init__(self, data_ingestion_config: DataIngestionConfig) -> None:
        try:
            # logging.info()
            self.data_ingestion_config = data_ingestion_config
        
        except Exception as e:
            raise SampleMLException(e, sys) from e
        
    def download_housing_data(self) -> str:
        try:
            # Download data from remote url
            download_url = self.data_ingestion_config.dataset_download_url

            # tarfile download directory
            tgz_download_dir = self.data_ingestion_config.tgz_download_dir

            os.makedirs(tgz_download_dir, exist_ok=True)

            download_file_name = os.path.basename(download_url)

            tgz_file_path = os.path.join(tgz_download_dir, download_file_name)

            logging.info(f'Downloading {download_file_name}')
            urllib.request.urlretrieve(
                url=download_url,
                filename=tgz_file_path
                )
            logging.info(f'{download_file_name} Saved at {tgz_download_dir}')

            return tgz_file_path



        except Exception as e:
            raise SampleMLException(e, sys) from e


    def extract_tgz_file(self, tgz_file_path) -> None:
        try:
            raw_data_dir = self.data_ingestion_config.raw_data_dir

            os.makedirs(raw_data_dir, exist_ok=True)

            logging.info(f'Extracting tgz file: [{tgz_file_path}]')
            with tarfile.open(tgz_file_path) as tgz_file:
                tgz_file.extractall(path=raw_data_dir)
            
            logging.info(f'Successfully Extracted at directory: [{raw_data_dir}]')

        except Exception as e:
            raise SampleMLException(e, sys) from e
        

    def train_test_split(self) -> DataIngestionArtifact:
        try:
            
            raw_data_dir = self.data_ingestion_config.raw_data_dir

            raw_data_file_name = os.listdir(path=raw_data_dir)[0]
            raw_data_file_path = os.path.join(raw_data_dir, raw_data_file_name)

            logging.info('Loading CSV File into Dataframe object')
            raw_data_frame = pd.read_csv(raw_data_file_path)
            logging.info('Succesfully Loaded CSV File')
            
            raw_data_frame['income_cat'] = pd.cut(
                x=raw_data_frame['median_income'],
                bins=[0.0, 1.5, 3.0, 4.5, 6.0, np.inf],
                labels=[1, 2, 3, 4, 5]
            )

            split = StratifiedShuffleSplit(
                n_splits=1,
                test_size=0.2,
                random_state=42
            )

            for train_index, test_index in split.split(raw_data_frame, raw_data_frame['income_cat']):
                strat_train_set = raw_data_frame.loc[train_index].drop(columns=['income_cat'])
                strat_test_set = raw_data_frame.loc[test_index].drop(columns=['income_cat'])

            train_file_path = os.path.join(self.data_ingestion_config.ingestion_train_dir, raw_data_file_name)
            test_file_path = os.path.join(self.data_ingestion_config.ingested_test_dir, raw_data_file_name)
            
            
            if strat_train_set is not None:
                os.makedirs(self.data_ingestion_config.ingestion_train_dir, exist_ok=True)
                strat_train_set.to_csv(train_file_path, index=False)
                is_train_ingested = True
            else:
                is_train_ingested = False

            if strat_test_set is not None:
                os.makedirs(self.data_ingestion_config.ingested_test_dir, exist_ok=True)
                strat_test_set.to_csv(test_file_path, index=False)
                is_test_ingested = True
            else:
                is_test_ingested = False

            return DataIngestionArtifact(
                train_data_path=train_file_path,
                test_data_path=test_file_path,
                is_ingested=is_train_ingested and is_test_ingested,
                message='Data Ingestion Completed Successfully.'
            )
        except Exception as e:
            raise SampleMLException(e, sys) from e
    
    def initiate_data_ingestion(self) -> DataIngestionArtifact:
        try:
            tgz_file_path = self.download_housing_data()
            self.extract_tgz_file(tgz_file_path)
            data_ingestion_artifact = self.train_test_split()
            return data_ingestion_artifact
        except Exception as e:
            raise SampleMLException(e, sys) from e