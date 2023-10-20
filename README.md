### Настройка:

Файл .env в корне проекта должен содержать опции (можно переименовать файл .env.example в .env):
    

    # URL API сервиса викторины
    URL_QUESTIONS_API=https://jservice.io/api/random?count=

    # Количество попыток повторных запросов к сервису в случае ошибки или дубликата вопроса
    RETRIES=3

    # Подключение к базе данных
    POSTGRES_SERVER=db
    POSTGRES_USER=user
    POSTGRES_PASSWORD=changeme
    POSTGRES_DB=questions

    # Интерфейс базы данных для тестовых целей
    PGADMIN_DEFAULT_EMAIL=admin@test.com
    PGADMIN_DEFAULT_PASSWORD=changeme

### Сборка:

    docker-compose -p demo-questions build

### Запуск

    docker-compose -p demo-questions up

### Сервис доступен по ссылке:

    http://127.0.0.1:8000

### Тестовый интерфейс для API по ссылке (Swagger UI):

    http://127.0.0.1:8000/docs

### Пример запроса:

    curl -X 'POST' \
    'http://127.0.0.1:8000/' \
    -H 'accept: application/json' \
    -H 'Content-Type: application/json' \
    -d '{
    "questions_num": 100
    }'

### Доступ к pgadmin4:


#### Ссылка на интерфейс:

    http://127.0.0.1:8000

#### Конфигурация (опционально):

    Файл pgadmin/.pgpass должен содержать имя и пароль к базе из .env

