'''Importing Libraries'''

import logging
import os
import sys
from os.path import join
from datetime import datetime
from typing import Any


LOG_FILE = f"{datetime.now().strftime('%Y-%m-%d_%H:%M:%S')}.log"
LOGS_DIR = 'logs'
LOG_FILE_PATH = join(LOGS_DIR, LOG_FILE)

os.makedirs(
    name=LOGS_DIR,
    exist_ok=True
)




logging.basicConfig(
    filename=LOG_FILE_PATH,
    filemode="w",
    format='[%(asctime)s] | %(levelname)s | %(filename)s | %(funcName)s() | %(lineno)d | %(message)s',
    level=logging.INFO
)

def get_log_dataframe(file_path: str) -> Any:
    '''Return pandas dataframe created from Logs directory.'''

    data=[]
    with open(file=file_path, encoding='utf-8') as log_file:
        for line in log_file.readlines():
            data.append(line.split("|"))
    try:
        import pandas as pd
    except ImportError as exc:
        logging.error('Pandas Module is Missing, Install it by `pip install pandas`.')
        raise ModuleNotFoundError('Missing Pandas Module. Install it by `pip install pandas`') from exc
    
    def get_dataframe(data: list) -> pd.DataFrame:
        '''Return a pandas dataframe after converting list of string into dataframe object.'''

        log_df = pd.DataFrame(data)
        log_df.columns = ["Time stamp","Log Level","line number","file name","function name","message"]

        log_df["log_message"] = log_df['Time stamp'].astype(str) +":$"+ log_df["message"]

        return log_df[["log_message"]]
    
    return get_dataframe(data)


