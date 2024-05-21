import whisper

# Загрузка модели
model = whisper.load_model("medium")  # Выбираем среднюю модель

# Загрузка аудиофайла
audio_path = "media/audio.mp3"
audio = whisper.load_audio(audio_path)

# Предварительная обработка аудиофайла (добавление или обрезание тишины, приведение к нужному формату и длительности)
audio = whisper.pad_or_trim(audio)

# Преобразование аудио в лог-мел-спектрограмму и передача на устройство модели
mel = whisper.log_mel_spectrogram(audio).to(model.device)

# Распознавание языка
language, _ = model.detect_language(mel)
print(f"Обнаруженный язык: {language}")

# Распознавание текста
result = model.transcribe(audio_path)
print("Распознанный текст:", result["text"])