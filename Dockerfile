FROM python:3.10

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY project ./project

# If you run with uvicorn:
CMD ["python", "-m", "project.main"]
