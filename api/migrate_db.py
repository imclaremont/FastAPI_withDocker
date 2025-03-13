from sqlalchemy import create_engine

from api.models.task import Base

DB_URL = "mysql+pymysql://root@db:3306/demo?charset=utf8" # 로컬에서 컨테이너 DB에 접속 시
# DB_URL = "mysql+pymysql://root:passwd@10.100.223.107:3306/demo?charset=utf8mb4” # RDE 환경 root/passwd로 접속 시

engine = create_engine(DB_URL, echo=True) # echo=True 옵션: SQL 실행 로그를 출력하도록 설정

def reset_database():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

if __name__== "__main__":
    reset_database()
