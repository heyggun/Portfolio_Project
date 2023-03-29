from fastapi import FastAPI
from pydantic import BaseModel
import time
from starlette.responses import JSONResponse
from utils.model.model import ALS
import traceback
from utils.config.logger import LogConfig
import warnings
import os
warnings.filterwarnings('ignore')

log = LogConfig()
app = FastAPI()
pid = os.getpid()

class memberInfo(BaseModel) :
    memNo : int
    ptrMemNo : int
    memSex : str
    isCallable : bool

# health_check api
@app.get('/_service_health_check')
async def health_check():
    return 1

@app.post('/recom')
async def recommendation(i : memberInfo) :
    req = time.time()
    recomm = {}
    try :
        log.Log(f'[API Request] pid : {pid} - memNo : {i.memNo} - ptrMemNo : {i.ptrMemNo} - isCallable : {i.isCallable}')
        als = ALS(i.memNo, i.memSex, i.ptrMemNo, i.isCallable)
        recomm = als.get_recomm()
    except Exception :
        # recomm['error'] = traceback.format_exc()
        trace_back = traceback.format_exc()
        log.error_log(f'[ERROR] [Failed Request - memNo : {i.profile["memNo"]}] \n {trace_back}')
    finally:
        recomm['restime'] = round(time.time() - req, 3)
        log.Log(f'[API Response] pid : {pid} - memNo : {i.memNo} - ptrMemNo : {i.ptrMemNo} - resCnt : ({len(recomm["topK"])}, {len(recomm["Sim"])}) - resTime : {round(time.time() - req, 3)}')

        return JSONResponse(recomm)

# uvicorn
# if __name__ == '__main__' :
#     uvicorn.run('recomm_start:app', host='0.0.0.0', port=1234, access_log=False,
#         reload_dirs=['/home/gguny/ai_data/recomm_data/dev/male'], reload=True)

