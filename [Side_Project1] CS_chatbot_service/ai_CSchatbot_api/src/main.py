from src.GetAnswer import *
from fastapi import FastAPI, Request, File, UploadFile
from pydantic import BaseModel
from typing import Optional, Union
from starlette.responses import JSONResponse
from utils.model.model import ChatbotModel
import uvicorn
import warnings
warnings.filterwarnings('ignore')
import torch, gc
import time
# import httpx
import asyncio



app = FastAPI()
# URL = "http://httpbin.org/uuid"
gc.collect()
torch.cuda.empty_cache()
ChatbotModel = ChatbotModel()
data, model = ChatbotModel.Load()

class userQA(BaseModel):
    question : Optional[str] = None

# async def request(client):
#     response = await client.get(URL)
#     return response.text

# async def task():
#     async with httpx.AsyncClient() as client:
#         tasks = [request(client) for i in range(100)]
#         result = await asyncio.gather(*tasks)
#         print(result)

# @app.get('/userQnA')
# async def main(question: Optional[str] = None):
#     GA = getAnswer(model, data)
#     answer = GA.return_answer(question)
#     result = {'answer': answer}
#     return JSONResponse(result)

@app.post('/userQnA')
async def main(userQA : userQA):
    # start = time()
    GA = getAnswer(model, data)
    answer = GA.return_answer(userQA.question)
    result = {'answer': answer}
    # await task()
    # print('time :', time()- start)
    return JSONResponse(result)
#
# @app.post('/files')
# async def create_upload_file(file: Union[UploadFile, None]= None):
#     if not file:
#         return {'message' : 'file error'}
#     else:
#         return {'filename' : file.filename}

if __name__ == '__main__':
   uvicorn.run('main:app', host="0.0.0.0", port=9000)

