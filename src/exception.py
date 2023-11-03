import sys
from src.logger import logging

def error_message_detail(error,error_detail:sys): 
    '''
    Whenever an exception gets raised.
    This function will take the exception (error) as input , and convert it to my custom message.
    '''
    _,_,exc_tb=error_detail.exc_info() # exc_tb variable will tell you about :-
    # In which line the error has occured.
    # In which file the erroe has occured.
    file_name=exc_tb.tb_frame.f_code.co_filename 
    error_message="Error occured in python script name [{0}] line number [{1}] error message[{2}]".format(
     file_name,exc_tb.tb_lineno,str(error))

    return error_message

    

class CustomException(Exception):
    def __init__(self,error_message,error_detail:sys):
        super().__init__(error_message)
        self.error_message=error_message_detail(error_message,error_detail=error_detail)
    
    def __str__(self):
        return self.error_message