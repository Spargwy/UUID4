Веб-сервер предназначенный для хранения файлов с тремя уровнями доступа: 

- Полностью приватный
- С доступом по-ссылке
- Открытый для всех

Инструкция:
-
- Склонировать репозиторий командой 
```
git clone https://github.com/Spargwy/UUID4
```

- Зайти в директорию UUID4
  
- Выполнить команду ```pip install requirements.txt``` для установки зависимостей

- Установить PostgreSQL и создать базу данных для проекта(ниже, в файле .env показана строка 
  для подключения к базе данных file_storage через пользователя postgres и пароль postgres). 

- Создать .env файл который будет содержать следующие поля:
```
BASE_URL=127.0.0.1:5000
DB_URL="postgresql://postgres:postgres@localhost:5432/file_storage"
SECRET=SECRET
```

- Создать и накатить миграции командами
```
flask db migrate
flask db upgrade
```

- Выполнить команду 
  ```export FLASK_APP=web_server```
  
- Запустить приложение командой 
```flask run```