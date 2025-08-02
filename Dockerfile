FROM python:3.13

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Обновляем пакеты и устанавливаем зависимости, нужные для pillow и сборки пакетов
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    libjpeg-dev \
    zlib1g-dev \
    libfreetype6-dev \
    liblcms2-dev \
    libtiff-dev \
    libwebp-dev \
    tcl8.6-dev \
    tk8.6-dev \
    python3-tk \
    && rm -rf /var/lib/apt/lists/*

# Копируем файлы, необходимые для установки зависимостей
COPY pyproject.toml poetry.lock* README.md /app/

# Устанавливаем poetry и зависимости Python
RUN pip install poetry && poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi

# Копируем весь проект в контейнер
COPY . /app/

COPY ./entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

CMD ["/entrypoint.sh"]
