# 1. Базовий образ
FROM python:3.10-slim

# 2. Системні бібліотеки (з виправленим libgl1)
RUN apt-get update && apt-get install -y \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# 3. Робоча папка
WORKDIR /app

# 4. Копіюємо файл вимог
COPY requirements.txt .

# 5. !!! МАГІЯ ТУТ !!!
# Спочатку примусово ставимо легкий PyTorch (CPU version).
# Це зекономить тобі 3 ГБ трафіку і купу нервів.
RUN pip install --no-cache-dir torch torchvision --index-url https://download.pytorch.org/whl/cpu

# 6. Тепер ставимо все інше (FastAPI, YOLO і т.д.)
# YOLO побачить, що PyTorch вже є, і не буде качати важку версію.
RUN pip install --no-cache-dir -r requirements.txt

# 7. Копіюємо код
COPY . .

# 8. Відкриваємо порт
EXPOSE 8000

# 9. Запуск
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]