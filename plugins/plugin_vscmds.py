# Команды управления visual studio
# author: Khasanov Murat

from vacore import VACore
import pyautogui

import sys
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

# функция на старте


def start(core: VACore):
    manifest = {
        "name": "Команды управления visual studio",
        "version": "1.0",
        "require_online": False,
        "commands": {
            "запуск кода|запусти код": run_file,
            "отладка|отладка кода|сделай отладку": debug_file,
            "вкладка": tab,
            "окно": window,
            "структура проекта|открой структуру проекта": structure_of_project,
            "поиск|поиск по коду": search,
            "глобальный поиск|глобальный поиск по коду": global_search,
            "пока": goodbye,
            "отформатировать код": format_code
        }
    }

    return manifest


def run_file(core: VACore, phrase: str):
    print("Команда запуск кода")
    pyautogui.hotkey(['Ctrl', 'f5'])


def debug_file(core: VACore, phrase: str):
    print("Команда отладки кода")
    pyautogui.press('f5')


def tab(core: VACore, phrase: str):
    print("Команда смены вкладки")
    pyautogui.hotkey(['ctrl', 'tab'])


def window(core: VACore, phrase: str):
    print("Команда смены окна")
    pyautogui.hotkey(['alt', 'tab'])


def structure_of_project(core: VACore, phrase: str):
    print("Команда открытия структуры проекта")
    pyautogui.hotkey(['ctrl', 'shift', 'e'])


def search(core: VACore, phrase: str):
    print("Команда поиск")
    pyautogui.hotkey(['ctrl', 'f'])


def global_search(core: VACore, phrase: str):
    print("Команда глобальный поиск")
    pyautogui.hotkey(['ctrl', 'shift', 'f'])


def goodbye(core: VACore, phrase: str):
    print("Программа завершается")
    sys.exit(0)  # Аргумент 0 означает нормальное завершение работы


def format_code(core: VACore, phrase: str):
    print("Команда форматирования кода")
    pyautogui.hotkey(['shift', 'alt', 'f'])

