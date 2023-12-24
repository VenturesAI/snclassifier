# Используем официальный образ Python как базовый
FROM python:3.10

# Устанавливаем рабочий каталог в контейнере
WORKDIR /usr/src/app

# Копируем файл зависимостей в рабочий каталог
COPY requirements.txt ./

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install collection
# Копируем все файлы проекта в рабочий каталог
COPY . .

# Указываем порт, на котором будет работать приложение
EXPOSE 8000

RUN mkdir -p /log/gunicorn
# Запускаем Gunicorn на порту 3000
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers=1", "snclassifier_djangoproject.wsgi:application"]