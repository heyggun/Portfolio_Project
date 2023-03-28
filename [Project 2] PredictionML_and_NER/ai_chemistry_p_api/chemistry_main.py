from fastapi import FastAPI
from pydantic import BaseModel
from predict import *
from datetime import datetime
from starlette.responses import JSONResponse
import traceback
import time
import os
from utils.config.logger import LogConfig
from utils.functions import *
import warnings
warnings.filterwarnings('ignore')

pid = os.getpid()
log = LogConfig()
app = FastAPI()
p = predictScore()

class memberInfo(BaseModel) :
    male : dict
    female : dict

# health_check api
@app.get('/_service_health_check')
async def health_check():
    return 1

@app.post('/chemistry')
async def chemi_score(info : memberInfo) :
    try:
        start = time.time()
        mem_no = info.male['memNo']
        ptr_mem_no = info.female['memNo']
        log.Log(f'[API Request] - pid : {pid} - memNo : {mem_no} - ptrMemNo : {ptr_mem_no}')

        df = make_base_dataframe(info.male, info.female)

        model_1_score, model_2_score, model_3_score, total_score = p.get_model_scores(df)
        result = {'gscore' : model_1_score, 'cscore' : model_2_score, 'mscore' : model_3_score,
                  'totalScore' : total_score, 'aiPid' : pid, 'aiTestDate' : str(datetime.today())[:10]}
    except Exception :
            trace_back = traceback.format_exc()
            log.error_log(f'[ERROR] [Failed Request - memNo : {mem_no} - ptrMemNo : {ptr_mem_no}] \n {trace_back}')
            result = {}
    finally:
        log.Log(f'[API Response] - pid : {pid} - {result} - Response Time : {time.time() - start:.3f}')
        return JSONResponse(result)

# if __name__ == '__main__':
#     uvicorn.run("chemi_score_main:app", host="0.0.0.0", port=8020) # log_config=LOGGING_CONFIG)
