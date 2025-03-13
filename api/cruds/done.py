from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select
from sqlalchemy.engine import Result

import api.models.task as task_model

def get_done(db: Session, task_id: int) -> task_model.Done | None:
    result: Result = db.execute(select(task_model.Done).filter(task_model.Done.id == task_id))
    return result.scalars().first()

def create_done(db: Session, task_id: int) -> task_model.Done:
    # task_id가 존재하는지 확인
    task = db.query(task_model.Task).filter(task_model.Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")  # ✅ 404 예외 발생
    
    # 존재하면 done 추가
    done = task_model.Done(id=task_id)
    db.add(done)
    db.commit()
    db.refresh(done)
    return done

def delete_done(db: Session, original: task_model.Done) -> None:
    db.delete(original)
    db.commit()
