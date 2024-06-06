from django.apps import AppConfig
from application_logging.logging_functions.general_system_logging import general_system_logger_generator


class MLBackendConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'MLBackend'
