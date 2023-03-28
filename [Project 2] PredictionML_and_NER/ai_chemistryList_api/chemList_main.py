from fastapi import FastAPI
from pydantic import BaseModel
from starlette.responses import JSONResponse
import traceback
from utils.config.logger import LogConfig
from get_rank import *
from utils.config.common import startPath
import time
import os
import warnings
warnings.filterwarnings('ignore')


pid = os.getpid()
log = LogConfig()
app = FastAPI()
log.Log(f'START PATH : {startPath}')
class searchInfo(BaseModel) :
    profile : dict
    searchType : str
    isCallable : bool

# health_check api
@app.get('/_service_health_check')
async def health_check():
    return 1

@app.post('/chem_list')
async def search(info : searchInfo) :
    try :
        start = time.time()
        log.Log(f'[API Request] pid : {pid} - memNo: {info.profile["memNo"]} - searchType : {info.searchType} - isCallable : {info.isCallable}')
        my_info = pd.DataFrame([info.profile])
        r = getRank(my_info, info.isCallable, info.searchType)
        result, log_cnt = r.get_rank()
        log.Log(f'[API Response] pid : {pid} - memNo : {info.profile["memNo"]} - searchType : {info.searchType} - ListCnt : {log_cnt} - Response Time : {time.time() - start:.3f}')
    except Exception :
        trace_back = traceback.format_exc()
        log.error_log(f'[ERROR] [Failed Request - memNo : {info.profile["memNo"]}] \n {trace_back}')
        result = {}
    finally :
        return JSONResponse(result)
#
# if __name__ == '__main__':
#     uvicorn.run("chemi_search_main:app", host="0.0.0.0", port=8021)