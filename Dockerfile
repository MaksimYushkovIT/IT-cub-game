# Используем официальный образ Python
FROM python:3.9-slim-buster

# Устанавливаем необходимые инструменты для сборки
RUN apt-get update && apt-get install -y \
    build-essential \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Устанавливаем рабочую директорию в контейнере
WORKDIR /app

# Копируем файлы зависимостей
COPY requirements.txt .

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем остальные файлы проекта
COPY . .

# Открываем порт, на котором работает приложение
EXPOSE 5000

RUN echo "#!/bin/sh\nsleep 5\nexec python run.py" > /entrypoint.sh && chmod +x /entrypoint.sh

CMD ["/entrypoint.sh"]