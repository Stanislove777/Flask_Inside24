# Flask_Inside24
Simple web app. REST API

## Используемые технологии (не включает дополнительные библиотеки)

|Технология|Версия|
|---|---|
|Python|3.8.5|
|SQLite3|3.37.0|
|Flask|2.1.3|

> Дополнительную информацию о используемых технологиях можно получить в файле inside24/requirements.txt

## Описание

В проекте реализован API по нескольким эндпоинтам, основное взаимодействие приложения заключается в работе с БД.
Приложение настроено на порт :5000

|Эндпоинт|Описание|
|---|---|
|```/api/login```|Эндпоинт принимает запрос с данными по пользователю (имя и пароль) в формате JSON. Производит проверку на присутствие данных, проверяет наличие пользователя в БД и выдает ответ со сгенерированным токеном jwt в формате JSON.|||
|```/api/message```|Эндпоинт принимает запрос с именем и текстом сообщения в формате JSON в теле сообщения и jwt токен, сгенерированный заранее в эндпоинте /api/login, в заголовке "token" со специальным префиксом "Bearer_". Производится декодирование пришедшего токена и проверка полученной даты через БД (имя пользователя). Если запрос проходит валидацию успешно, то выполняется сохранение сообщения присланное пользователем в БД. Если сообщение соответсвует шаблону "history <num_msg>", где <num_msg> число от 0 до 999, возвращает историю в кол-ве <num_msg> последних сообщений данного пользователя.|||

### SQL схема

```sql

CREATE TABLE messages (
id INTEGER PRIMARY KEY,
name TEXT NOT NULL,
text TEXT NOT NULL,
user_id INTEGER NOT NULL,
FOREIGN KEY (user_id)
REFERENCES users (id));

CREATE TABLE users (
id INTEGER PRIMARY KEY,
name TEXT NOT NULL,
password NOT NULL);

```

### Примеры запросов/ответов

#### ```/api/login```

Запрос:
```bash
curl -X POST -H "Content-Type: application/json" -d '{"name": "Client", "password": "654321"}' http://localhost:5000/api/login
```

Ответ:
```json
{"token":"eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJuYW1lIjoiQ2xpZW50In0.X3mjhe_xUzD1PnrNMocVO-A6j9NZqy0s1AVsFMBFSN0"}
```

#### ```/api/message```

Запрос (сохранение сообщения):
```bash
curl -X POST -H "Content-Type: application/json" -H "token: Bearer_eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJuYW1lIjoiQ2xpZW50In0.X3mjhe_xUzD1PnrNMocVO-A6j9NZqy0s1AVsFMBFSN0" -d '{"name": "Client", "message": "histo"}' http://localhost:5000/api/message
```

Ответ:
```json
{"description":"Message saved","status":"SUCCESS"}
```

Запрос (вывод истории):
```bash
curl -X POST -H "Content-Type: application/json" -H "token: Bearer_eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJuYW1lIjoiQ2xpZW50In0.X3mjhe_xUzD1PnrNMocVO-A6j9NZqy0s1AVsFMBFSN0" -d '{"name": "Client", "message": "history 10"}' http://localhost:5000/api/message
```

Ответ:
```bash
[["Client","histo"],["Client","histo"],["Client","My_text_message"],["Client","my history 10"],["Client","histo"],["Client","histo"],["Client","My_text_message"],["Client","my history 10"],["Client","My_text_message"],["Client","my history 10"]]
```

Также, дополнительно имеется файл с запросами inside24/curl_rq.txt

## Запуск приложения

Приложение можно запустить несколькими способами:

- В дериктории inside24 выполнить команду:

```bash
python3 inside24.py
```

- Через запуск Docker контейнера выполнить команду:

```bash
docker-compose up --build
```

### Запуск тестов

В директории inside24/ выполнить команду:

```bash
python3 inside24_tests.py 
```

Покрытие тестами осуществлялось как с позитивным сценарием, так и с негативным.
