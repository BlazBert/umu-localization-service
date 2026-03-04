# syntax=docker/dockerfile:1
FROM python:3.12-slim

# Keep logs flowin’ & builds slim
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# 1) Install crew (deps)
COPY requirements.txt .
RUN pip install -r requirements.txt

# 2) Copy code & booty
COPY app/ .

# 3) Open the hatch & set sail
EXPOSE 80
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]