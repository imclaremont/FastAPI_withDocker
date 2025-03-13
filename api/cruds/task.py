from sqlalchemy.orm import Session
from sqlalchemy import select
from sqlalchemy.engine import Result

import api.models.task as task_model
import api.schemas.task as task_schema

def create_task(
        # 스키마 task_create: task_schema, TaskCreate를 인수로 받는다
        db: Session, task_create: task_schema.TaskCreate) -> task_model.Task:
            task = task_model.Task(**task_create.model_dump()) # 이를 DB 모델인 task_model.Task로 변환한다
            db.add(task)
            db.commit() # DB에 커밋한다
            db.refresh(task) # task를 업데이트한다(작성된 레코드의 ID를 가져옴)
            return task # 생성한 DB 모델을 반환

def get_tasks_with_done(db: Session) -> list[tuple[int, str, bool]]:
    result: Result = db.execute(
            select(
                task_model.Task.id,
                task_model.Task.title,
                (task_model.Done.id.isnot(None)).label("done")
            ).outerjoin(task_model.Done) # 메인 DB 모델에 조인할 모델을 지정
    )
    return result.all()

def get_task(db: Session, task_id: int) -> task_model.Task | None:
    result: Result = db.execute( select(task_model.Task).where(task_model.Task.id == task_id))
    return result.scalars().first()

def update_task(
    db: Session, task_create: task_schema.TaskCreate, original:task_model.Task) -> task_model.Task:
    original.title = task_create.title
    db.add(original)
    db.commit()
    db.refresh(original)
    return original

def delete_task(db: Session, original: task_model.Task) -> None:
    db.delete(original)
    db.commit()