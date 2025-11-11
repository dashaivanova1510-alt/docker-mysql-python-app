FROM python:3.9-slim

# Встановлюємо робочу директорію всередині контейнера
WORKDIR /usr/src/app

# Копіюємо файл залежностей та встановлюємо їх
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Копіюємо решту файлів застосунку
COPY . .

CMD [ "python", "./app.py" ]
