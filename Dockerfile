FROM python:3.12-slim
RUN groupadd -r mydjangosite && useradd -r -g mydjangosite mydjangosite

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

RUN pip install --no-cache-dir --upgrade pip
WORKDIR /app/www/sitewomen
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

USER mydjangosite