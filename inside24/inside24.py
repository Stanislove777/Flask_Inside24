from flask import Flask, jsonify, request
import jwt
import re
import db_conn

app = Flask(__name__)

'''
Эндпоинт /api/login принимает запрос с данными по пользователю (имя и пароль) в формате JSON.
Производит проверку на наличие данных, проверяет наличие пользователя в БД и выдает ответ со сгенерированным токеном jwt в формате JSON. 
'''
@app.route("/api/login", methods=['POST'])
def login_user():
    # сбор данных из запроса - имя и пароль
    rq_body = request.json
    _name = rq_body['name']
    _pass = rq_body['password']

    # проверка на наличие данных
    if not _name or not _pass:
        return jsonify(status="ERROR", description="Name or password NOT FOUND in request")
    
    # поиск данных по БД
    if db_conn.verify_data(_name, _pass):
        # генерация токена с записью в него имени пользователя
        _token = jwt.encode(payload={"name": _name}, key='secret_key')
        # отправка ответа с токеном
        return jsonify(token=_token), 200
    return jsonify(status="ERROR", description="User INVALID")

'''
Эндпоинт /api/message принимает запрос с именем и текстом сообщения в формате JSON в теле сообщения и jwt токен, сгенерированный заранее в эндпоинте /api/login, в заголовке "token" со специальным префиксом "Bearer_".
Производится декодирование пришедшего токена и проверка полученной даты через БД (имя пользователя).
Если запрос проходит валидацию успешно, то выполняется сохранение сообщения присланное пользователем в БД.
Если сообщение соответсвует шаблону "history <num_msg>", где <num_msg> число от 0 до 999, возвращает историю в кол-ве <num_msg> последних сообщений данного пользователя. 
'''
@app.route("/api/message", methods=['POST'])
def send_message():
    # сбор данных из запроса - токен (заголовок), имя и сообщение (тело). 
    # Дополнительно: форматирование заголовка с токеном без префикса
    rq_body = request.json
    _token = request.headers['token']
    _token = _token[7:]
    _name = rq_body['name']
    _msg = rq_body['message']

    # Декодирование токена и получение имени пользователя
    try:
        data = jwt.decode(_token, key='secret_key', algorithms=['HS256', ])
    except jwt.exceptions.InvalidTokenError as error:
            print("Error decode: ", error)
            return jsonify(status="ERROR", description="Decode ERROR")
    
    # проверка принадлежности токена пользователю чье сообщение
    if data == {"name": _name}:
        # проверка пользователя в БД и получение его идентификатора в БД (id)
        user_data = db_conn.verify_data(_name, None)

        if user_data:
            # проверка сообщения на команду получения истории пользователя
            match = re.search(r'^history\s\d{1,3}$', _msg)

            if match:
                # получение кол-ва сообщений для истории пользователя
                num_msg = match[0].split()
                # получение истории из БД
                history = db_conn.get_history(_name, num_msg[1])

                # проверка наличия запрашиваемой истории
                if history:
                    return jsonify(history), 200
                else:
                    return jsonify(status="ERROR", description="History NOT FOUND"), 200
            else:
                # сохранение сообщения в БД
                db_conn.save_msg(_name, _msg, user_data[0])
                return jsonify(status="SUCCESS", description="Message saved"), 200
    return jsonify(status="ERROR", description=data), 200

if __name__ == "__main__":
    app.run()