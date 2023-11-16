from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# Установка дефолтной настройки Django для Celery
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

app = Celery('core')

# Использование настроек Django для конфигурации Celery
app.config_from_object('django.conf:settings', namespace='CELERY')

# Поиск и загрузка всех задач Celery в приложениях Django
app.autodiscover_tasks()