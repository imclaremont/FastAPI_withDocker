# db.py 파일은 SQLAlchemy를 사용하여 데이터베이스 엔진을 생성하고, 세션을 관리하며, ORM 모델의 기반이 되는 Base 클래스를 정의하는 설정 파일
# SQLAlchemy의 세션은 "DB 연결을 관리하는 객체", 트랜잭션을 유지하고 실행하는 역할을 한다

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DB_URL = "mysql+pymysql://root@db:3306/demo?charset=utf8" # 로컬에서 컨테이너 DB에 접속 시
# DB_URL = "mysql+pymysql://root:passwd@10.100.223.107:3306/demo?charset=utf8mb4” # RDE 환경 root/passwd로 접속 시

db_engine = create_engine(DB_URL, echo=True)
db_session = sessionmaker(autocommit=False, autoflush=False, bind=db_engine)
SessionLocal = db_session

Base = declarative_base()

def get_db():
    db = SessionLocal() # 세션 인스턴스 생성
    try:
        yield db
    finally:
        db.close() # 요청이 끝난 후 세션 종료