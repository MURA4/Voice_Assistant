# Скачивание файлов из репозитория с git
# author: Khasanov Murat

import subprocess
import sys
import os

username = 'Mura4'
foldername = 'example'

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
    print("Загрузка кода с гита...")
    subprocess.run("rd /s /Q example", shell=True, text=True) #удаление внутренностей папки и самой папки без подтверждения
    subprocess.run("git clone git@github.com:%(username)s/%(foldername)s.git" % {"username": username, "foldername": foldername}, shell=True, text=True) #копирование 
    subprocess.run("exit()", shell=True, text=True)


