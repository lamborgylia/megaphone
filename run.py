import os
import sys
import subprocess
import threading
import time

# Получаем абсолютный путь к корневой директории проекта
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def run_django():
    """Запускает Django сервер"""
    os.chdir(os.path.join(BASE_DIR, 'megaphone'))  # Переходим в директорию с manage.py
    python_path = os.path.join('venv', 'Scripts', 'python.exe')
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mega_site.settings')
    subprocess.run([python_path, 'manage.py', 'runserver'])

if __name__ == '__main__':
    # Запускаем Django
    run_django() 