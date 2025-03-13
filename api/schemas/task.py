# 이 Task 클래스는 할 일(Task) 정보를 담는 데이터 모델로 사용
# BaseModel은 Pydantic에서 데이터 검증을 위한 기본 클래스, Field()는 필드 값을 설정하는 함수
from pydantic import BaseModel, Field
from typing import Optional # 변수가 특정 타입이거나 None일 수도 있음을 명시하는 타입 힌트 기능

# 공통 필드를 포함하는 부모 클래스 TaskBase 를 정의 (공통 필드: title)
class TaskBase(BaseModel):
    title: Optional[str] = Field(None, example=" 세탁소에 맡긴 것을 찾으러 가기")
    # str | None -> title 값은 문자열이거나 None이 될 수 있음
    # Field 기본값은 None, Swagger UI 에서 " " 내용을 예제 값으로 표시

# 일반적으로 POST 함수에서는 id를 지정하지 않고 DB에서 자동으로 id를 매기는 경우가 많다
# 또한 done 필드에서도 Task 작성 시에는 항상 false 이므로, POST /tasks 의 엔드포인트에서 제외
class TaskCreate(TaskBase):
    pass # TaskBase를 상속받아 추가적인 필드 없이 그대로 사용 가능

class TaskCreateResponse(TaskCreate):
    id: int

    class Config:
        from_attributes = True # ORM 모델(SQLAlchemy) 또는 일반 객체에서 데이터를 변환할 때 사용

# 할 일 데이터를 조회할 때 사용하는 모델(TaskBase를 상속받아 title 필드를 포함)
class Task(TaskBase): 
    id: int
    done: bool = Field(False, description="완료 플래그")
    # description은 FastAPI 자동 문서화(/docs)에 설명으로 표시됨

    class Config:
        from_attributes = True # ORM 모델(SQLAlchemy) 또는 일반 객체에서 데이터를 변환할 때 사용

class TaskResponse(Task):
    pass