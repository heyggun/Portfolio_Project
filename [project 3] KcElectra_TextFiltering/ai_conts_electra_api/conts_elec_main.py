import time
import uvicorn
import traceback
from fastapi import FastAPI
from pydantic import BaseModel
from predict import predictModel
from typing import Optional, List, Set, Union
from utils.config.common import conf
from utils.config.logger import LogConfig
from starlette.responses import JSONResponse

mu_model = predictModel(conf.ModelPath1)
call_model = predictModel(conf.ModelPath2)

log = LogConfig()
app = FastAPI()


class UserData(BaseModel):
    autoNo: int
    memNo: int
    mateConts: Optional[str]
    familyConts: Optional[str]


class getContents(BaseModel):
    UserInfo: Union[List[UserData], None] = None


# health_check api ~
@app.get('/_service_health_check')
async def health_check():
    return 1


@app.post('/conts_filter')
async def conts_filter(i: getContents):
    user_dict = i.dict()['UserInfo']
    result_list = list()
    log.Log(f" Request - {user_dict}")

    for idx in range(len(user_dict)):
        req = time.time()
        result = {'autoNo': user_dict[idx]['autoNo'], 'memNo': user_dict[idx]['memNo']}
        try:
            if user_dict[idx]['mateConts']:
                result['matePred'] = [mu_model.predict_sentence(user_dict[idx]['mateConts']),
                                      call_model.predict_sentence(user_dict[idx]['mateConts'])]
            if user_dict[idx]['familyConts']:
                result['familyPred'] = [mu_model.predict_sentence(user_dict[idx]['familyConts']),
                                        call_model.predict_sentence(user_dict[idx]['familyConts'])]
        except Exception as e:
            result['matePred'] = [0, 0]
            result['familyPred'] = [0, 0]
            log.error_log(traceback.format_exc())
        finally:
            if 'matePred' not in result.keys():
                result['matePred'] = [1, 0]
            if 'familyPred' not in result.keys():
                result['familyPred'] = [1, 0]
            # print(f"Elapsed Time : {time.time() - req:.2f}")
            result['reqTime'] = round(time.time() - req, 3)
            result_list.append(result)

    log.Log(f"Response - {result_list}")
    return JSONResponse(result_list)

# uvicorn
# if __name__ == '__main__' :
#     uvicorn.run('conts_filter_main:app', host='0.0.0.0', port=1234, access_log=False,
#         reload=True)