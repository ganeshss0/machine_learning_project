import os
import sys


class SampleMLException(Exception):
    '''Main Exception Class of Sample ML Project'''
    def __init__(self, error: Exception, error_detail: sys):
        super().__init__(error, error_detail)
        
        self.error_message = self.get_detailed_error_message(error, error_detail)
    
    @staticmethod
    def get_detailed_error_message(error: Exception, error_detail: sys) -> str:
        '''
        error_message: Exception object
        error_detail: object of sys module
        '''
        _, _, exec_tb = error_detail.exc_info()

        line_number = exec_tb.tb_lineno
        file_name = exec_tb.tb_frame.f_code.co_filename

        error = f'''
        Error occured in script: 
        [{file_name}] at 
        line number {line_number}] 
        error message: [{error}]
        '''

        return error
    
    def __str__(self):
        return self.error_message
    
    def __repr__(self):
        return str(SampleMLException.__name__)
