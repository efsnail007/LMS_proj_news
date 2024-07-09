# NEWS&VIEWS

Блог-платформа для ведения персональных блогов и новостей

Для запуска необходимо подготовить файл .env:
```
SECRET_KEY=<ключ>
DEBUG=0
ALLOWED_HOSTS=127.0.0.1 localhost
CSRF_TRUSTED_ORIGINS=http://127.0.0.1 http://localhost
POSTGRES_DB=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_HOST=postgres
POSTGRES_PORT=5432
EMAIL_HOST=<smpt-сервер>
EMAIL_PORT=<порт>
EMAIL_USE_TLS=<0 или 1 в зависимости от smpt-сервера>
EMAIL_USE_SSL=<0 или 1 в зависимости от smpt-сервера>
EMAIL_HOST_USER=<пользователь smpt-сервера>
EMAIL_HOST_PASSWORD=<пароль>
```

Далее необходимо использовать команду:
```
docker-compose build
```

Затем необходимо написать:
```
docker-compose up
```
