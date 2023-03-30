from sentence_transformers import SentenceTransformer
from starlette.responses import JSONResponse
from utils.config.logger import LogConfig
from utils.model.answer import ChatModel
from typing import Optional
from pydantic import BaseModel
from datetime import datetime
from fastapi import FastAPI
import traceback, time, os, uvicorn, warnings
warnings.filterwarnings('ignore')

pid = os.getpid()
log = LogConfig()
app = FastAPI()
Chat = ChatModel()


class UserQA(BaseModel) :
    autoNo: int
    memNo: int
    question: Optional[str]

# health_check api
@app.get('/_service_health_check')
async def health_check():
    return 1

@app.post('/chatbot')
async def chatbot(user : UserQA) :
    log.Log(f'[API Request] - pid : {pid} - autoNo : {user.autoNo} - memNo : {user.memNo} - Question : {user.question}')
    result_dict= dict()

    try:
        start = time.time()
        result_dict['autoNo'] = user.autoNo
        result_dict['memNo'] = user.memNo
        result_dict['answer'] = Chat.getAnser(user.question)

    except Exception :
            trace_back = traceback.format_exc()
            result_dict['autoNo'] = user.autoNo
            result_dict['memNo'] = user.memNo
            result_dict['answer'] = '고객센터 문의'
            log.error_log(f'[ERROR] [Failed Request - pid : {pid} - '
                          f'autoNo : {user.autoNo} - memNo : {user.memNo} - Question : {user.question}] \n {trace_back}')

    finally:
        log.Log(f'[API Response] - pid : {pid} - autoNo : {user.autoNo} - memNo : {user.memNo}  -'
                f'Answer : {result_dict} - Response Time : {time.time() - start:.3f}')
        result_dict['restime'] = time.time() - start
        return JSONResponse(result_dict)

if __name__ == '__main__':
    uvicorn.run("chatbot_main:app", host="0.0.0.0", port=1234) # log_config=LOGGING_CONFIG)
