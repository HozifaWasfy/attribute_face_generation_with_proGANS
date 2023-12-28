FROM tiangolo/uvicorn-gunicorn-fastapi:python3.11

WORKDIR /app 

COPY . .

RUN pip install --upgrade pip

RUN pip install -r req-backend.txt

EXPOSE 8000

CMD [ "python", "run_backend.py" ]