FROM python:3.10
ADD . /code
WORKDIR /code
RUN pip install -r requirements.txt
CMD ["uvicorn","api:app","--reload", "--host","0.0.0.0","--port","8000"]