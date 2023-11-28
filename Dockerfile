# Используйте официальный образ Python как базовый
FROM python:3.8

# Установите рабочую директорию в контейнере
WORKDIR /usr/src/app

# Скопируйте файл зависимостей и установите зависимости
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Скопируйте ваш Django-проект в контейнер
COPY . .

# Соберите статические файлы
RUN python manage.py collectstatic --noinput

# Команда для запуска Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "core.wsgi:application"]