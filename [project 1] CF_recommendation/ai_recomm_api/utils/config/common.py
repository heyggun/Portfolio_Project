import getpass
import os
from buffalo.algo.als import ALS
import warnings
warnings.filterwarnings('ignore')

##############################################################################################
# PATH configure
##############################################################################################


userName = getpass.getuser()
startPath = os.getcwd() # start_api file Execution Path
localUserPath = f'D:/pyproject/ai_recomm_api'
serverUserPath = f'/home/{userName}'

# api name
apiName = "ai_recomm"
# model name
modelMale = 'male/als_model_male'
modelFemale = 'female/als_model_female'
# server data conf
serverApiDataPath = "recomm_data" # data path

##############################################################################################
# Configure Class
##############################################################################################
class BasicConfig:
    # port
    port = 1234
    # log path
    serverLogPath = "LOGS" + '/' + apiName + '_api'
    logPath = serverUserPath + '/' + serverLogPath + '/' + apiName
    # ai_data path - file load path
    dataPath = serverUserPath + '/ai_data/' + serverApiDataPath
    modelMale = dataPath + '/' + modelMale
    modelFemale = dataPath + '/' + modelFemale

class DevConfig():
    # port
    port = 1234
    # log path
    serverDevLogPath = "LOGS_devel" + '/' + apiName + '_api'
    logPath = serverUserPath + '/' + serverDevLogPath + '/' + apiName
    # ai_data path - file load path
    dataPath = serverUserPath + '/ai_data/' + serverApiDataPath + '/dev'
    modelMale = dataPath + '/' + modelMale
    modelFemale = dataPath + '/' + modelFemale

class DevTestConfig():
    port = 1234
    # log path
    serverDevLogPath = "LOGS_devel" + '/' + apiName + '_api'
    logPath = serverUserPath + '/' + serverDevLogPath + '/' + apiName + "_test"
    # ai_data path - file load path
    dataPath = serverUserPath + '/ai_data/' + serverApiDataPath + '/dev'
    # server dev/dev_test path
    modelMale = dataPath + '/' + modelMale
    modelFemale = dataPath + '/' + modelFemale

class LocalConfig():
    # port
    port = 1234
    # data conf
    localApiDataPath = 'D:/pyproject/ai_recomm_api/utils'  # data path
    # log path
    localLogPath = localApiDataPath + "/log"
    logPath = localUserPath + '/' + localLogPath + '/' + apiName
    dataPath = localApiDataPath + '/model'
    # ai_data path - file load path
    modelMale = dataPath + '/' + modelMale
    modelFemale = dataPath + '/' + modelFemale

##############################################################################################
# 실행 위치에 따른 api 가동
serverPath = serverUserPath + "/API/" + apiName + "_api"
serverDevPath = serverUserPath + "/API_devel/" + apiName + "_api"
serverDevTestPath = serverUserPath + "/API_devel/" + apiName + "_api_test"

if userName == "gguny":
    if startPath == serverPath:
        conf = BasicConfig()
    elif startPath == serverDevPath:
        conf = DevConfig()
    else:
        conf = DevTestConfig()
else:
    conf = LocalConfig()

m_model = ALS()
m_model.load(conf.modelMale)
f_model = ALS()
f_model.load(conf.modelFemale)

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
    #a15, a16 gconf
    gconf = {"bind": f"0.0.0.0:{conf.port}",
             "workers" : 1,
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

    elif startPath == serverDevTestPath:
        # a15_dev_test
        gconf['bind'] = f"0.0.0.0:{conf.port}"
        gconf['workers'] = 1
        gconf['pidfile'] = pidFilePath_test

    return gconf