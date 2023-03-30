from sentence_transformers import SentenceTransformer
from numpy.linalg import norm
from numpy import dot
import pandas as pd
import numpy as np
import getpass
import os
import warnings
warnings.filterwarnings('ignore')

##############################################################################################
# PATH configure
##############################################################################################

# user name ex) local : "PC", server : "yeoai"
userName = getpass.getuser()
startPath = os.getcwd() # start_api file Execution Path
localUserPath = f'D:/pyproject/ai_chatbot'
serverUserPath = f'/home/{userName}'


# api name
apiName = "ai_chatbot"
# Embedding data
Data = 'chatEmbedding.npy'
# server data conf
serverApiDataPath = "ai_chatbot_data" # data path

##############################################################################################
# Configure Class
##############################################################################################

class BasicConfig():
    # port
    port = 1234
    # log path
    serverLogPath = "LOGS" + '/' + apiName + '_api'
    logPath = serverUserPath + '/' + serverLogPath + '/' + apiName
    # ai_data path - file load path
    serverModelPath = serverUserPath + '/ai_data/' + serverApiDataPath
    embeddingPath = serverModelPath + '/' + Data


class DevConfig():
    # port
    port = 1234
    # log path
    serverDevLogPath = "LOGS_devel" + '/' + apiName + '_api'
    logPath = serverUserPath + '/' + serverDevLogPath + '/' + apiName
    # ai_data path - file load path
    serverModelPath = serverUserPath + '/ai_data/' + serverApiDataPath
    embeddingPath = serverModelPath + '/' + Data

class DevTestConfig():
    port = 1234
    # log path
    serverDevLogPath = "LOGS_devel" + '/' + apiName + '_api'
    logPath = serverUserPath + '/' + serverDevLogPath + '/' + apiName + "_test"
    # ai_data path - file load path
    serverModelPath = serverUserPath + '/ai_data/' + serverApiDataPath
    # server dev/dev_test path
    embeddingPath = serverModelPath + '/' + Data


class LocalConfig():
    # port
    port = 1234
    # data conf
    localApiDataPath = 'D:/project/ai_report/utils/data/'  # data path
    # log path
    localLogPath = localApiDataPath + "/log"
    logPath = localUserPath + '/' + localLogPath + '/' + apiName
    localModelPath = 'D:/project/ai_report/utils/model/'
    # ai_data path - file load path
    embeddingPath = localModelPath + '/' + Data


##############################################################################################
# 실행 위치에 따른 api 가동

serverPath = serverUserPath + "/API/" + apiName + "_api"
serverDevPath = serverUserPath + "/API_devel/" + apiName + "_api"
serverDevTestPath = serverUserPath + "/API_devel/" + apiName + "_api_test"


if userName == "gguny":
    if startPath == serverDevTestPath:
        conf = DevTestConfig()
    elif startPath == serverDevPath:
        conf = DevConfig()
    else:
        conf = BasicConfig()
else:
    conf = LocalConfig()

Model = SentenceTransformer('sentence-transformers/xlm-r-100langs-bert-base-nli-stsb-mean-tokens')
Embedding = pd.DataFrame(np.load(conf.embeddingPath, allow_pickle=True), columns= ['question','answer','embedding'])

##############################################################################################
# Uvicorn configure - 유비콘 사용시
##############################################################################################
def Uconf():
    uconf = {
        "host" : "0.0.0.0",
        "port" : conf.port
    }
    if startPath == serverDevPath:
        uconf['port'] = conf.port
    elif startPath == serverDevTestPath:
        uconf['port'] = conf.port
    return uconf

##############################################################################################
# Gunicorn configure - 구니콘 사용시
##############################################################################################
# gunicorn pid path
pidFilePath = f"/var/run/gguny/{apiName}.pid"
pidFilePath_dev = f"/var/run/gguny/{apiName}_dev.pid"
pidFilePath_test = f"/var/run/gguny/{apiName}_dev_test.pid"

def Gconf():
    gconf = {"bind": f"0.0.0.0:{conf.port}",
             "workers" : 2,
             "worker_class" : "uvicorn.workers.UvicornWorker",
             "pidfile" : pidFilePath,
             "user" : 1000,
             "group" : 1000
     }
    if startPath == serverDevPath:
        gconf['bind'] = f"0.0.0.0:{conf.port}"
        gconf['workers'] = 1
        gconf['pidfile'] = pidFilePath_dev

    elif startPath == serverDevTestPath:
        gconf['bind'] = f"0.0.0.0:{conf.port}"
        gconf['workers'] = 1
        gconf['pidfile'] = pidFilePath_test

    return gconf