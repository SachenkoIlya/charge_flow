FROM python:3.11-slim

# системные зависимости
RUN apt-get update && apt-get install -y build-essential libpq-dev && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# зависимости Python
COPY requirements.txt requirements.txt
RUN pip install --upgrade pip && pip install -r requirements.txt

# весь код проекта
COPY frontend ./frontend
COPY core ./core


# значение CMD переопределяется в docker-compose
CMD ["python", "-m", "frontend.main"]