from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# устанавливаем переменную окружения с именем файла настроек проекта Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'NewsPaper.settings')

app = Celery('news')

# используем конфигурации Django для настройки Celery
app.config_from_object('django.conf:settings', namespace='CELERY')

# автоматически обнаруживаем и регистрируем задачи в приложениях Django
app.autodiscover_tasks()

