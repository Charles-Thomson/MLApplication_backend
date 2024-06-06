from django.apps import AppConfig
from application_logging.logging_functions.general_system_logging import general_system_logger_generator
import logging 

class ApiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'API'

    def ready(self):
        try:
            general_system_logger_generator()
        except Exception as e :
            print(f"Error generating the system logger at run time - Error {e}")
            
        general_system_logger = logging.getLogger("general_system_logger")
        general_system_logger.info(f"CREATED LOGGER")