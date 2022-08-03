import sqlite3


'''
Проверка данных пользователя в БД
'''
def verify_data(name, password):
    try:
        connection = sqlite3.connect("DataBase.db")
        print("... DB connection SUCCESS ...")
        if password:
            result = connection.execute("SELECT id, name, password FROM users WHERE password = ? AND name = ?",
            (password, name),).fetchone()
        else:
            result = connection.execute("SELECT id, name FROM users WHERE name = ?",
            (name,),).fetchone()
        print("... Verify data: ", result, " ...")
        if result:
            return result
        return None
    except sqlite3.Error as error:
        print("Error SQLite3: ", error)
    finally:
        if (connection):
            connection.close()
            print("... DB connection CLOSED ...")

'''
Сохранение сообщения пользователя в БД
'''
def save_msg(name, message, user_id):
    try:
        connection = sqlite3.connect("DataBase.db")
        print("Sql connection SUCCESS")
        connection.execute("INSERT INTO messages (name, text, user_id) VALUES (?, ?, ?)",
        (name, message, user_id,),)
        connection.commit()
        print("Message saved SUCCESS")
    except sqlite3.Error as error:
        print("Error SQLite3: ", error)
    finally:
        if (connection):
            connection.close()
            print("Sql connection closed")

'''
Получение истории сообщений пользователя
'''
def get_history(name, num_msg):
    try:
        connection = sqlite3.connect("DataBase.db")
        print("Sql connection SUCCESS")
        results = connection.execute("SELECT name, text FROM messages WHERE name = ? ORDER BY id DESC LIMIT ?",
        (name, num_msg,),).fetchall()
        print("... HISTORY: ", results)
        if results:
            return results
        return None
    except sqlite3.Error as error:
        print("Error SQLite3: ", error)
    finally:
        if (connection):
            connection.close()
            print("Sql connection closed")