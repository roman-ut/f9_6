# Запуск

1. Установка и запуск базы данных

docker build -t image . && docker run -itd -p 5432:5432 --name container image

2. Установка компонентов и запуск приложения 

````
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python main.py
````

Сервер будет доступен по адресу http://localhost:8080/