from decimal import Decimal
import os
from dataclasses import dataclass
from typing import Optional, Union

from ....config.enums.logs.log_levels import LOG_LEVELS
from ....utils.logging.loggers.app_config import ApplicationConfigLogger

@dataclass
class Settings:
    ''' Base class that holds and validates a set 
        of configuration values for the application 
    '''

    FLASK_SETTINGS_KEY = "APP_SETTINGS"
    # Name of the configuration group - overridden by subclasses
    GROUP_NAME = 'Base'
    # Default log level for data in this group
    DEFAULT_LOG_LEVEL = LOG_LEVELS.INFO

    @staticmethod
    def read_config_from_env_or_default( 
        env_var: str,
        data_type: type = str,
        default_value: Optional[str] = None
    ) -> Union[bool, int, str, list[str], Decimal, bytes, None]:
        ''' Read the configuration from an environmental variable
            and cast to the values to the specified data type
        '''
        
        # Get the value from the environment or get the default
        value = os.environ.get(env_var, default_value)
        if value is None:
            return None

        # Cast the data to the proper type
        parsed_value = Settings._normalize_config_value_type(value, data_type)
        return parsed_value
    

    @staticmethod
    def _normalize_config_value_type(value:str, data_type:type) -> Union[bool, int, str, list[str], Decimal, bytes]:
        if data_type == bool:
            parsed_value = value.lower() in ["true", "1", "yes"]
        elif data_type == int:
            parsed_value = int(value)
        elif data_type == list:
            parsed_value = [x.strip() for x in str(value).split(',')]
        elif data_type == Decimal:
            parsed_value = Decimal(value)
        elif data_type == bytes:
            parsed_value = value.encode()
        else:
            parsed_value = str(value)

        return parsed_value
    

    def _log_configuration_value(self, field_name:str, field_metadata:dict):
        ''' Log the read configuration value at the log level specified in the 
            field's metadata. For example:
            {'log_level': 'warn'} or {'log_level': None} to not log at all
        '''

        if self._should_log_config(field_metadata):
            log_message = field_metadata.get("log_message")
            log_level = field_metadata.get("log_level", self.DEFAULT_LOG_LEVEL)
            if not log_message:
                log_message = f"    {field_name} = {getattr(self, field_name)}"

            logger = getattr(ApplicationConfigLogger, log_level)
            logger(log_message)


    def _should_log_config(self, metadata:dict) -> bool:
        ''' Returns True if the field metadata indicates it should be logged '''

        return "log_level" not in metadata or metadata.get("log_level") != None


    def _configure_logger(self, log_level:str):
        if log_level:
            ApplicationConfigLogger.create_logger(log_level)


    def __post_init__(self):
        ''' Log all configuration values '''

        ApplicationConfigLogger.warn(f'[{self.GROUP_NAME} Configuration]')
        for field_info in self.__dataclass_fields__.values():
            self._log_configuration_value(field_info.name, field_info.metadata)
