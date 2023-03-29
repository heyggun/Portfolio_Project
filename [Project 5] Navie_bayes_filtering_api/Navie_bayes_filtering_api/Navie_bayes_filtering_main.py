from fastapi import FastAPI
from pydantic import BaseModel
from predict import predictModel
from typing import Optional, List, Set, Union
from utils.config.common import conf
from utils.config.logger import LogConfig
from starlette.responses import JSONResponse
import time
import uvicorn
import traceback
import os
import warnings
warnings.filterwarnings('ignore')


log = LogConfig()
app = FastAPI()


class UserConts(BaseModel):
    autoNo: int
    memNo: int
    Contents: Optional[str]


# health_check api ~
@app.get('/_service_health_check')
async def health_check():
    return 1


@app.post('/navie_filter')
async def dalla_filter(i: UserConts):
    print(i.dict())
    log.Log(f" Request - {i.dict()}")
    req = time.time()
    result = i.dict()
    conts = i.dict()['Contents']
    del result['Contents']

    try:
        PM = predictModel()
        result['adYN'] = PM.predict_sentence(conts)

    except Exception as e:
        result['adYN'] = 0
        log.error_log(traceback.format_exc())
    finally:
        result['reqTime'] = round(time.time() - req, 3)
        log.Log(f"Response - {result}")
        print(result)

    return JSONResponse(result)

uvicorn
if __name__ == '__main__' :
    uvicorn.run('Navie_bayes_filtering_main:app', host='0.0.0.0', port=1234, access_log=False,
        reload=True)