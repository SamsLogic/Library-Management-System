import logging
from logging.config import dictConfig
import os
from config.config import LOGS_FILE_PATH

os.makedirs(LOGS_FILE_PATH, exist_ok=True)

LOGGING = {
    'version':1,
    'formatters':{
        'standard':{
            'class':'logging.Formatter',
            'format':'%(asctime)s [%(levelname)s] %(name)s: %(message)s'
        },
    },
    'handlers':{
        'console': {
            'class': 'logging.StreamHandler',
            'level': 'DEBUG',
            'formatter': 'standard',
        },
        'file': {
            'class': 'logging.handlers.RotatingFileHandler',
            'maxBytes': 1024*1024*1,
            'backupCount': 1,
            'level': 'DEBUG',
            'formatter': 'standard',
            'filename': os.path.join(LOGS_FILE_PATH, 'Books.log')
        }
    },
    'loggers':{
        'db':{
            'handlers': ['file','console'],
            'level':'INFO',
            'propagate':True
        },
        'services':{
            'handlers': ['file','console'],
            'level':'DEBUG',
            'propagate':True
        }
    }
}
    
dictConfig(LOGGING)
db_logger = logging.getLogger('db')
services_logger = logging.getLogger('services')