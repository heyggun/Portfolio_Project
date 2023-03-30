import getpass
import os
import joblib
import warnings
warnings.filterwarnings('ignore')

##############################################################################################
# PATH configure
##############################################################################################

# user name ex) local : "PC", server : "yeoai"
userName = getpass.getuser()
startPath = os.getcwd() # start_api file Execution Path
localUserPath = f'D:/recommendation/RRS'
serverUserPath = f'/home/{userName}'

# api name
apiName = "ai_rrs"
# model name
modelName = 'PR_model.pkl'
# server data conf
serverApiDataPath = "rrs_data/" # data path

##############################################################################################
# Configure Class
##############################################################################################

class BasicConfig:
    # port
    port = 8060
    # log path
    serverLogPath = "LOGS" + '/' + apiName + '_api'
    logPath = serverUserPath + '/' + serverLogPath + '/' + apiName
    # ai_data path - file load path
    dataPath = serverUserPath + '/ai_data/' + serverApiDataPath
    # modelPath = serverUserPath + '/ai_data/' + modelName


class DevConfig():
    # port
    port = 8860
    # log path
    serverDevLogPath = "LOGS_devel" + '/' + apiName + '_api'
    logPath = serverUserPath + '/' + serverDevLogPath + '/' + apiName
    # ai_data path - file load path
    dataPath = serverUserPath + '/ai_data/' + serverApiDataPath


class LocalConfig():
    # port
    port = 8060
    # data conf
    localApiDataPath = f'D:/recommendation/RRS'  # data path
    # log path
    localLogPath = localApiDataPath + "/log"
    logPath = localUserPath + '/' + localLogPath + '/' + apiName
    # ai_data path - file load path
    dataPath = f'D:/recommendation/RRS/utils/data/'

##############################################################################################
# 실행 위치에 따른 api 가동
serverPath = serverUserPath + "/API/" + apiName + "_api"
serverDevPath = serverUserPath + "/API_devel/" + apiName + "_api"

##############################################################################################
# 실행 위치에 따른 api 가동
serverPath = serverUserPath + "/API/" + apiName + "_api"
serverDevPath = serverUserPath + "/API_devel/" + apiName + "_api"
serverDevTestPath = serverUserPath + "/API_devel/" + apiName + "_api_test"

if userName == "yeoai":
    if startPath == serverPath:
        conf = BasicConfig()
    elif startPath == serverDevPath:
        conf = DevConfig()
    else:
        conf =DevConfig()

else:
    conf = LocalConfig()


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
    return uconf

##############################################################################################
# Gunicorn configure - 구니콘 사용시
##############################################################################################
# gunicorn pid path
pidFilePath = f"/var/run/yeoai/{apiName}.pid"
pidFilePath_dev = f"/var/run/yeoai/{apiName}_dev.pid"
pidFilePath_test = f"/var/run/yeoai/{apiName}_dev_test.pid"

def Gconf():
    #a15, a16 gconf
    gconf = {"bind": f"0.0.0.0:{conf.port}",
             "workers" : 4,
             "worker_class" : "uvicorn.workers.UvicornWorker",
             "pidfile" : pidFilePath,
             "user" : 1000,
             "group" : 1000
     }
    if startPath == serverDevPath:
        # a15_dev
        gconf['bind'] = f"0.0.0.0:{conf.port}"
        gconf['workers'] = 1
        gconf['pidfile'] = pidFilePath_dev

    return gconf