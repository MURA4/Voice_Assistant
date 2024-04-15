# Скачивание файлов из репозитория с git
# author: Khasanov Murat

from git import Repo
import sys
import os

# URL репозитория на GitHub
repo_url = 'https://github.com/MURA4/example'

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))
from vacore import VACore

# функция на старте
def start(core:VACore):
    manifest = {
        "name": "Скачивание файлов из репозитория с git",
        "version": "1.0",
        "require_online": False,
        "commands": {
            "скачай|скачай код с гита": download_from_git,
        }
    }

    return manifest

def download_from_git(core:VACore, phrase: str):
    # Указываем путь к папке, куда хотим клонировать репозиторий
    destination_folder = r'C:\\Users\\ferge\\OneDrive\\Desktop\\DIPLOM\\example'

    # Клонирование репозитория
    try:
        Repo.clone_from(repo_url, destination_folder)
        print(f"Репозиторий успешно клонирован в {destination_folder}")
    except Exception as e:
        print(f"Произошла ошибка при клонировании: {e}")


