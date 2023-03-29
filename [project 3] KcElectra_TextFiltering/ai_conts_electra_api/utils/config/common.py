import getpass
import os

userName = getpass.getuser()
startPath = os.getcwd() # start_api file Execution Path
localUserPath = 'D:/pyproject/NLP/conts_filtering_api'
serverUserPath = f'/home/{userName}'

# api name
apiName = "ai_conts_electra"
# model name
modelName1 = 'mu_model.pt'
modelName2 = 'call_model.pt'
# server data conf
serverApiDataPath = "conts_electra_api" # data path

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
    ModelPath1 = serverModelPath + '/' + modelName1
    ModelPath2 = serverModelPath + '/' + modelName2


class DevConfig():
    # port
    port = 1234
    # log path
    serverDevLogPath = "LOGS_devel" + '/' + apiName + '_api'
    logPath = serverUserPath + '/' + serverDevLogPath + '/' + apiName
    # ai_data path - file load path
    serverModelPath = serverUserPath + '/ai_data/' + serverApiDataPath
    ModelPath1 = serverModelPath + '/' + modelName1
    ModelPath2 = serverModelPath + '/' + modelName2

class LocalConfig():
    # port
    port = 1234
    # data conf
    localApiDataPath = f'{localUserPath}/utils/data'  # data path
    # log path
    localLogPath = localApiDataPath + "/log"
    logPath = localUserPath + '/' + localLogPath + '/' + apiName
    # model path
    localModelPath = f'{localUserPath}/utils/model'
    # ai_data path - file load path
    ModelPath1 = localModelPath + '/' + modelName1
    ModelPath2 = localModelPath + '/' + modelName2


##############################################################################################
# 실행 위치에 따른 api 가동
serverPath = serverUserPath + "/API/" + apiName + "_api"
serverDevPath = serverUserPath + "/API_devel/" + apiName + "_api"


if userName == "gguny":
    if startPath == serverDevPath:
        conf = DevConfig()
    else:
        conf = BasicConfig()
else:
    conf = LocalConfig()



##############################################################################################
# Gunicorn configure
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

    return gconf