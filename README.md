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

|Эндпоинт|Описание|
|---|---|
|```/api/login```|Эндпоинт принимает запрос с данными по пользователю (имя и пароль) в формате JSON. Производит проверку на присутствие данных, проверяет наличие пользователя в БД и выдает ответ со сгенерированным токеном jwt в формате JSON.|||
|```/api/message```|Эндпоинт принимает запрос с именем и текстом сообщения в формате JSON в теле сообщения и jwt токен, сгенерированный заранее в эндпоинте /api/login, в заголовке "token" со специальным префиксом "Bearer_". Производится декодирование пришедшего токена и проверка полученной даты через БД (имя пользователя). Если запрос проходит валидацию успешно, то выполняется сохранение сообщения присланное пользователем в БД. Если сообщение соответсвует шаблону "history <num_msg>", где <num_msg> число от 0 до 999, возвращает историю в кол-ве <num_msg> последних сообщений данного пользователя.|||

### Примеры запросов/ответов

#### ```/api/login```

Запрос:
> ```curl -X POST -H "Content-Type: application/json" -d '{"name": "Client", "password": "654321"}' http://localhost:5000/api/login```

Ответ:
> ```{"token":"eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJuYW1lIjoiQ2xpZW50In0.X3mjhe_xUzD1PnrNMocVO-A6j9NZqy0s1AVsFMBFSN0"}```

#### ```/api/message```

Запрос (сохранение сообщения):
> ```curl -X POST -H "Content-Type: application/json" -H "token: Bearer_eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJuYW1lIjoiQ2xpZW50In0.X3mjhe_xUzD1PnrNMocVO-A6j9NZqy0s1AVsFMBFSN0" -d '{"name": "Client", "message": "histo"}' http://localhost:5000/api/message```

Ответ:
> ```{"description":"Message saved","status":"SUCCESS"}```

Запрос (вывод истории):
>```curl -X POST -H "Content-Type: application/json" -H "token: Bearer_eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJuYW1lIjoiQ2xpZW50In0.X3mjhe_xUzD1PnrNMocVO-A6j9NZqy0s1AVsFMBFSN0" -d '{"name": "Client", "message": "history 10"}' http://localhost:5000/api/message```

Ответ:
> ```[["Client","histo"],["Client","histo"],["Client","My_text_message"],["Client","my history 10"],["Client","histo"],["Client","histo"],["Client","My_text_message"],["Client","my history 10"],["Client","My_text_message"],["Client","my history 10"]]```

Также, дополнительно имеется файл с запросами inside24/curl_rq.txt

## Запуск приложения

Приложение можно запустить несколькими способами:

- В дериктории inside24 выполнить команду:

``` python3 inside24.py ```

- Через запуск Docker контейнера выполнить команду:

``` docker-compose up --build ```

### Запуск тестов

В директории inside24/ выполнить команду:

``` python3 inside24_tests.py ```

Разработано некоторое кол-во тестов как с позитивным сценарием, так и с негативным.
