from fastapi import FastAPI
from api.routers import task, done # api 디렉터리 속 routers 디렉터리의 task.py, done.py 모듈 가져오기
import uvicorn

app = FastAPI() # app은 FastAPI의 인스턴스
app.include_router(task.router) # task 모듈의 API 라우트를 FastAPI 앱에 추가
app.include_router(done.router) # done 모듈의 API 라우트를 FastAPI 앱에 추가
# task.router / done.router 는 각각 task / done 모듈에서 정의된 APIRouter 인스턴스

@app.get("/")
async def root():
    return {"message": "Welcome to the FastAPI server!"}

@app.get("/hello")
async def hello():
    return {"message": "hello world!"}

if __name__ == "__main__": # 직접 로컬로 실행하는 경우에만 실행하는 함수
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
