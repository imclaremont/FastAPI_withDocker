# Docker 정의 파일
# 사용할 공개 이미지를 가져와 Poetry를 사용해 패키지 정의 파일인 pyproject.toml을 기반으로 각 python 패키지를 설치

# python3.11 기반 이미지 다운로드
FROM python:3.11-buster

# 출력 버퍼링 해제(로그가 실시간으로 출력되도록 설정)
ENV PYTHONUNBUFFERED=1

# 작업 디렉토리 설정
WORKDIR /src

# pip로 poetry 설치
RUN pip install poetry

# poetry 관련 파일 복사(존재하는 경우)
COPY pyproject.toml* poetry.lock* ./

# poetry 가상환경을 프로젝트 내부(.venv)에 생성하도록 설정
RUN poetry config virtualenvs.in-project true
RUN if [ -f pyproject.toml ]; then poetry install --no-root; fi

# uvicorn 서버 실행
ENTRYPOINT ["poetry", "run", "uvicorn", "api.main:app", "--host", "0.0.0.0", "--reload"]