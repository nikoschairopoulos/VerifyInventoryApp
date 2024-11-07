#######################################
# At this module we will define all the 
# logging configurations
#######################################

import os 
from pathlib import Path



#current directory (is the parent)
CURRENT_DIRECTORY = Path(__file__).parent.absolute()

#Add log files (relative paths)
log_file_component = 'logs/components.logs'

#current file to log
path_file_log = CURRENT_DIRECTORY / log_file_component


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
        },
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': path_file_log,
        },
        'rotating_file': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': 'app.log',
            'maxBytes': 1024 * 1024,  # 1 MB
            'backupCount': 5,
        },
    },
    'loggers': {
        'component': {
            #'handlers': ['console', 'file', 'rotating_file'],
            'handlers':['file'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'serialzers':{
            'handlers': ['console'],
            'level': 'INFO',  # Control the minimum level for myapp logger
            'propagate': False,
        }
    }
}