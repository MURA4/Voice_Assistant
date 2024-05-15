# Голосовой ассистент Катя

Катя - русский голосовой ассистент для работы оффлайн. Требует Python 3.5+ (зависимость может быть меньше, но в любом случае Python 3)

Поддерживает плагины (скиллы)

### Установка

1. Для быстрой установки всех требуемых зависимостей можно воспользоваться командой:
```pip install -r requirements.txt```

2. Для запуска запустите файл **runva_vosk.py** из корневой папки.
По умолчанию он запустит оффлайн-распознаватель vosk для распознавания речи с микрофона, 
и pyttsx движок для озвучивания ассистента 
[Подробнее о pyttsx здесь](https://github.com/nateshmbhat/pyttsx3).

3. После запуска проверить можно простой командой - скажите "Катя, привет!" в микрофон

### Общая логика

Запуск всех команд начинается с имени ассистента (настраивается в options/core.json, по умолчанию - Катя). 
Так сделано, чтобы исключить неверные срабатывания при постоянном прослушивании микрофона.
Далее будут описываться команды без префикса "Катя".

### Плагины

Поддержка плагинов сделана на движке [Jaa.py](https://github.com/janvarev/jaapy) - минималистичный однофайловый движок поддержки плагинов и их настроек.

Плагины располагаются в папке plugins и должны начинаться с префикса "plugin_".

Настройки плагинов, если таковые есть, располагаются в папке "options" (создается после первого запуска).

### Активные плагины/скиллы (уже в папке plugins)

Для каждого плагина написано, требуется ли онлайн. 
Для отключения удалите из папки

**plugin_greetings.py** - приветствие (оффлайн). Пример команды: "катя, привет"

**plugin_mediacmds.py** - команды управления медиа (оффлайн). Пример: "дальше, громче, тише, сильно громче, сильно тише, пауза".
Если установлено mpcIsUseHttpRemote, то сначала делается попытка вызвать команду MPC HC плейера, если не удается - используется эмуляция мультимедийных клавиш

**plugin_mpchcmult.py** - проигрывание мультиков через MPC-HC из определенной папки (оффлайн). Пример "мультик <название_мультика>". Папка задается в конфиге. 
При вызове команды в папке ищется файл с соответствующим названием <название_мультика> и любым расширением. Если найден - запускается на проигрывание.
(Так что можно делать свою базу данных мультов, вместо ютуба с непонятными алгоритмами ранжирования)

**plugin_timer.py** - таймер (оффлайн). Примеры: "таймер, таймер шесть минут, таймер десять секунд"

**plugin_weatherowm.py** - погода (онлайн). Примеры: "погода, погода завтра, погода послезавтра, прогноз погоды". 
Требует установки в конфиге бесплатного API-ключа с https://openweathermap.org/ , а также местоположения

**plugin_yandex_rasp.py** - расписание ближайших электричек через Яндекс.Расписания. Пример: "электричка, электрички".
Требует установки в конфиге бесплатного API-ключа для личных нужд (до 500 запросов в сутки) с https://yandex.ru/dev/rasp/raspapi/ , а также станций отправления и назначения

---

**plugin_tts_pyttsx.py** -  (оффлайн) позволяет делать TTS (Text-To-Speech, озвучку текста) через pyttsx движок. Используется по умолчанию.

**plugin_tts_console.py** -  (оффлайн) заглушка для отладки. Вместо работы TTS просто выводит текст в консоль.

### Неактивные скиллы (plugins_inactive)

Для работы перенесите в папку plugins

**plugin_simpleyandexmusic.py** - открывает страницу Яндекс.Музыки и запускает её. Пример: "запусти радио, запусти музыку"

**plugin_wikipediasearch.py** - поиск в Википедии. Пример: "википедия кошка, вики собака". Читает первые два абзаца, если найдено. (Inspired by @EnjiRouz)

**plugin_youtubesearch.py** - поиск на Ютубе. Пример: "ютуб остров сокровищ". Открывает страницу в браузере с поиском. (Inspired by @EnjiRouz)

**plugin_tts_silero.py** - (оффлайн) TTS через Silero. При первом запуске требует онлайна, чтобы скачать файл с нейросетью. 
Требует pytorch 1.9+. На мой взгляд, работает немного медленно + не озвучивает числа, требуя их перевода в числительные + шипит. Тем не менее, очень крут!
Голос задается в конфиге.

### Настройки ядра (core.json)

Настройки конкретных плагинов лучше смотреть в плагинах

```
{
    "isOnline": true, # при установке в false будет выдавать заглушку на команды плагинов, требующих онлайн. Рекомендуется, если нужен только оффлайн.
    "logPolicy": "cmd", # all|cmd|none . Когда распознается речь с микрофона - выводить в консоль всегда | только, если является командой | никогда
    "mpcHcPath": "C:\\Program Files (x86)\\K-Lite Codec Pack\\MPC-HC64\\mpc-hc64_nvo.exe", # путь до MPC HC, если используете
    "mpcIsUse": true, # используется ли MPC HC?
    "mpcIsUseHttpRemote": true, # MPC HC - включено ли управление через веб-интерфейс?
    "ttsEngineId": "pyttsx", # используемый TTS-движок
    "v": "1.7", # версия плагина core. Обновляется автоматически, не трогайте
    "voiceAssNames": "Катя|Екатерина|Катюша" # Если это появится в звуковом потоке, то дальше будет команда. (Различные имена помощника, рекомендуется несколько)
}
```

### Отладка и разработка (для разработчиков)

Для отладки можно использовать запуск системы через файл **runva_cmdline.py**. 

Она делает запуск ядра (**VACore in vacore.py**) через интерфейс командной строки, это удобнее, чем голосом диктовать.

* Подключить собственный навык можно, создав плагин в **plugins_**. Смотрите примеры.
* Подключить собственный TTS можно плагином. Как примеры, смотрите plugins_tts_console.py, plugins_tts_pyttsx.py.
* Также, создав собственный **runvoice_** файл, можно, при желании, подключить свойт Speech-To-Text движок.

### Speech-to-Text через SpeechRecognition

SpeechRecognition - классический движок для запуска распознавания через Google и ряд других сервисов.
Для запуска этого распознавания запустите систему через файл **runva_speechrecognition.py**.

Для работы потребуется:

`pip install PyAudio`

`pip install SpeechRecognition`

Если есть проблемы с установкой PyAudio, прочтите детали [у EnjiRouz](https://github.com/EnjiRouz/Voice-Assistant-App/blob/master/README.md)

**Особенности:** распознавание числительных. Одна и та же фраза распознается так:
* VOSK: таймер десять секунд
* SpeechRecognition (Google): таймер 10 секунд 

### Благодарности

@EnjiRouz за проект голосового ассистента: https://github.com/EnjiRouz/Voice-Assistant-App, который стал основой (правда, был очень сильно переработан)

AlphaCephei за прекрасную библиотеку распозавания Vosk ( https://alphacephei.com/vosk/index.ru ) 




# Voice_Assistant
