FROM tiangolo/uvicorn-gunicorn-fastapi:python3.11

WORKDIR /app 

COPY . .

RUN pip install --upgrade pip

RUN pip install -r requirments.txt

EXPOSE 8000

CMD [ "uvicorn", "backend/backend:app" ]