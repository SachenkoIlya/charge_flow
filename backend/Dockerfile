FROM python:3.11-slim

# системные зависимости
RUN apt-get update && apt-get install -y build-essential libpq-dev && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# зависимости Python
COPY requirements.txt requirements.txt
RUN pip install --upgrade pip && pip install -r requirements.txt

# весь код проекта
COPY backend ./backend
COPY core ./core

CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]