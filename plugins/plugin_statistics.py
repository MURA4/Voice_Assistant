# Информация о системе
# author: Murat Khasanov

import socket
import psutil

from vacore import VACore

def start(core: VACore):
    manifest = {
        "name": "Информация о системе",
        "version": "1.0",
        "require_online": False,

        "commands": {
            "выведи мой ай пи|выведи мой эй пи":  get_local_ip,
            "выведи загрузку процессора|выведи загрузка процессора": get_cpu_load,
            "выведи дисковое пространство": get_disk_usage,
            "выведи информацию о системе": get_full_info
        }
    }

    return manifest

def get_full_info(core: VACore, manifest: dict):
    get_local_ip
    get_cpu_load
    get_disk_usage

def get_local_ip_helper(core: VACore, manifest: dict):
    try:
        # Создаем сокет
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # Устанавливаем соединение с удаленным сервером (в данном случае Google DNS)
        s.connect(('8.8.8.8', 80))
        # Получаем локальный IP-адрес
        local_ip = s.getsockname()[0]
        return local_ip
    except Exception as e:
        print("Ошибка при получении локального IP-адреса:", e)
        return None


def get_local_ip(core: VACore, manifest: dict):
    # Вызываем функцию для получения локального IP-адреса и выводим результат
    local_ip = get_local_ip_helper(core, manifest)
    if local_ip:
        print("Локальный IP-адрес вашего компьютера:", local_ip)
    else:
        print("Не удалось получить локальный IP-адрес")


def get_cpu_load_helper(core: VACore, manifest: dict):
    try:
        # Получаем информацию о загрузке процессора
        cpu_load = psutil.cpu_percent(interval=1, percpu=False)
        return cpu_load
    except Exception as e:
        print("Ошибка при получении загрузки процессора:", e)
        return None
    # Вызываем функцию для получения загрузки процессора и выводим результат


def get_cpu_load(core: VACore, manifest: dict):
    cpu_load = get_cpu_load_helper(core, manifest)
    if cpu_load is not None:
        print("Загрузка процессора: {:.2f}%".format(cpu_load))
    else:
        print("Не удалось получить загрузку процессора")


def get_disk_usage_helper(core: VACore, manifest: dict):
    try:
        # Получаем информацию о дисковом пространстве
        disk_usage = psutil.disk_usage('/')
        # Получаем процент доступного дискового пространства
        available_percent = disk_usage.percent
        return available_percent
    except Exception as e:
        print("Ошибка при получении информации о дисковом пространстве:", e)
        return None


def get_disk_usage(core: VACore, manifest: dict):
    # Вызываем функцию для получения процента доступного дискового пространства и выводим результат
    available_percent = get_disk_usage_helper(core, manifest)
    if available_percent is not None:
        print("Доступное дисковое пространство: {:.2f}%".format(
            available_percent))
    else:
        print("Не удалось получить информацию о дисковом пространстве")

# def get_system_info(core: VACore, phrase: str):
#     # cmd = "top -bn1 | grep load | awk '{printf \"%.2f\", $(NF-2)}'"
#     # CPU = subprocess.check_output(cmd, shell = True )
#     # cmd = "free -m | awk 'NR==2{printf \"%s/%s %.2f%%\", $3,$2,$3*100/$2 }'"
#     # MemUsage = subprocess.check_output(cmd, shell = True )
#     # cmd = "df -h | awk '$NF==\"/\"{printf \"%d/%d %s\", $3,$2,$5}'"
#     # Disk = subprocess.check_output(cmd, shell = True)

#     # text = "АйПи адресс: " + str(IP[0:-2]).replace(".", " точка ").replace("b'", " ") + " !"
#     # core.play_voice_assistant_speech(text)

#     # text = "Загрузка процессора " + str(CPU).replace("b'", " ") + " !"
#     # core.play_voice_assistant_speech(text)

#     mem = get_values_from(str(MemUsage))
#     text = "Свободно оперативной памяти {0} из {1} {2}".format(mem[0], mem[1], compute_suffix(mem[1], ["мегабайтов", "мегабайт", "мегабайта"]))
#     percent = int(round(float(mem[2].replace("'", ""))))
#     text = text + "Что составляет {0} {1} от доступного объема памяти".format(percent, compute_suffix(str(percent), ["процентов", "процент", "процента"]))
#     core.play_voice_assistant_speech(text)

#     dsk = get_values_from(str(Disk))
#     text = "Свободно на носителе {0} из {1} {2}".format(dsk[0], dsk[1], compute_suffix(mem[1], ["гигабайтов", "гигабайт", "гигабайта"]))
#     percent = int(round(float(dsk[2].replace("'", ""))))
#     text = text + "Что составляет {0} {1} от доступного объема памяти".format(percent, compute_suffix(str(percent), ["процентов", "процент", "процента"]))
#     core.play_voice_assistant_speech(text)
