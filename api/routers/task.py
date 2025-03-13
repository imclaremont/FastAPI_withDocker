# api/routers/task.py 파일은 경로 동작 함수들을 모아놓은 파일
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

import api.models.task as task_model
import api.schemas.task as task_schema
import api.cruds.task as task_crud

from api.db import get_db

router = APIRouter()

# 클라이언트가 GET /tasks 요청을 보내면 list_tasks() 함수가 실행
@router.get("/tasks", response_model=list[task_schema.Task]) # 할 일 목록을 조회하는 API
def list_tasks(db: Session = Depends(get_db)):
    tasks = db.query(task_model.Task).all()
    return [task_schema.Task(id=task.id, title=task.title, done=bool(task.done)) for task in tasks]

@router.post("/tasks", response_model=task_schema.TaskCreateResponse)
async def create_task(task_body: task_schema.TaskCreate, db: Session = Depends(get_db)):
    return task_crud.create_task(db, task_body)
# task_body.dict()의 결과는 { "title": "세탁소에 맡긴 것을 찾으러 가기" } 형태의 딕셔너리
# **task_body.dict()는 이 딕셔너리의 키-값 쌍을 함수 호출 시 개별 인수로 전달
# 즉, task_schema.TaskCreateResponse(id=1, title=task_body.title, done=task_body.done)라고 작성하는 것과 동일

@router.put("/tasks/{task_id}", response_model=task_schema.TaskCreateResponse)
async def update_task(task_id: int, task_body: task_schema.TaskCreate, db: Session = Depends(get_db)):
    task = task_crud.get_task(db, task_id=task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task_crud.update_task(db, task_body, original=task)

@router.delete("/tasks/{task_id}", response_model=None)
async def delete_task(task_id: int, db: Session = Depends(get_db)):
    task = task_crud.get_task(db, task_id=task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    
    task_crud.delete_task(db, original=task)
    return {"message": f"Task {task_id} deleted successfully"}