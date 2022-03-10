FROM python:3.8.12-buster

COPY api /api
COPY Model_DeepAgri.joblib Model_DeepAgri.joblib
COPY requirements.txt requirements.txt

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

CMD uvicorn api.api:app --host 0.0.0.0 --port $PORT
