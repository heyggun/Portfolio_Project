import logging
import logging.handlers
import logging.config
from utils.config.common import conf
logPath = conf.logPath

mainLog = logPath + "_main.log"
errorLog = logPath + "_error.log"
gAccessLog = logPath + "_gaccess.log"
gErrorLog = logPath + "_gerror.log"

LOGGING_CONFIG: dict = {
    "version": 1,
    "disable_existing_loggers": False,

    "root":{
        "level": "INFO",
        "handlers": ["console"]
    },
    "loggers":{
        "error": {
            "level": "INFO",
            "handlers": ["error"],
            "propagate": True,
            "qualname": "error"
        },

        "gunicorn.access": {
            "level": "INFO",
            "handlers": ["gunicorn.access"],
            "propagate": True,
            "qualname": "gunicorn.access"
        },
        "gunicorn.error": {
            "level": "ERROR",
            "handlers": ["gunicorn.error"],
            "propagate": True,
            "qualname": "gunicorn.error"
        }
    },
    "formatters": {
        "generic": {
            "format": "%(levelname)s : %(asctime)s - %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",
            "class": "logging.Formatter"
        },
        "access": {
            "format": "[%(asctime)s] - [PID : %(process)d] - [REQUEST : %(message)s]",
            "class" : "logging.Formatter"
        }
    },
    "handlers": {
        "console": {
            "class": "logging.FileHandler",
            "formatter": "generic",
            "filename": mainLog
        },
        "error": {
            "class": "logging.FileHandler",
            "formatter": "generic",
            "filename": errorLog
        },
        "gunicorn.access": {
            "class": "logging.FileHandler",
            "formatter": "access",
            "filename": gAccessLog
        },
        "gunicorn.error": {
            "class": "logging.FileHandler",
            "formatter": "generic",
            "filename": gErrorLog
        }
    },
}
logging.config.dictConfig(LOGGING_CONFIG)

# 로그에 request, message 표시
class LogConfig:
    def __init__(self):
        pass

    def Log(self, message):
        uvicorn = logging.getLogger("root")
        uvicorn.info(message)

    def error_log(self, error_message):
        error = logging.getLogger("error")
        error.info(error_message)
