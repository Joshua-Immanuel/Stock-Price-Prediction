import sys
def error_message_detail(error,error_detail:sys):
   _,_, exc_tb = error_detail.exc_info()
   error_message=f"error occured in script name {exc_tb.tb_frame.f_code.co_filename} in line number {exc_tb.tb_lineno} error message {str(error)}"
   return error_message

class CustomException(Exception):
   def __init__(self, error_message,error_detail:sys):
      super().__init__(error_message)
      self.error_message=error_message_detail(error_message,error_detail=error_detail)

   def __str__(self):
      return self.error_message
   


# try:
#    a=5/0
# except:
#    logger.logging.info('division by 0')
#    raise CustomException('divided by 0',sys)