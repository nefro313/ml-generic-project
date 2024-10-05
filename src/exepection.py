import sys

"""This is where the custom message error will look like """
def error_message_details(error,error_detail:sys):
    _,_,exc_tb = error_detail.exc_info()
    filname = exc_tb.tb_frame.f_code.co_filename
    error_message = 'Error is occured in python script file name [{0}] line number [{1}] error message [{2}]'.format(
        filname,
        exc_tb.tb_lineno,
        str(error)
    )
    return error_message

class CustomExpection(Exception):
    def __init__(self,error_message,error_detail:sys):
        super().__init__(error_message)
        self.error_message = error_message_details(error_message,error_detail=error_detail)
        
    def __str__(self):
        return self.error_message


