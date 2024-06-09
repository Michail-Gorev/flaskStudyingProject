import sqlite3


class FDataBase:
    def __init__(self, db):
        self.__db = db
        self.__cursor = db.cursor()

    def getUsers(self):
        sql_request = '''SELECT * FROM user'''
        try:
            self.__cursor.execute(sql_request)
            res = self.__cursor.fetchall()
            if res: return res
        except:
            print('Ошибка при чтении Базы Данных')
        return []

    def getBuildings(self):
        sql_request = '''SELECT * FROM buildings'''
        try:
            self.__cursor.execute(sql_request)
            res = self.__cursor.fetchall()
            if res: return res
        except:
            print('Ошибка при чтении Базы Данных')
        return []

    def addUser(self, username, email, pass_hash, gender, is_confirmed):
        unique_email = True
        try:
            self.__cursor.execute(f"SELECT COUNT() as `count` FROM user WHERE email LIKE '{email}'")
            res1 = self.__cursor.fetchone()
            self.__cursor.execute(f"SELECT COUNT() as `count` FROM user WHERE username LIKE '{username}'")
            res2 = self.__cursor.fetchone()
            if res1['count'] > 0:
                print("Пользователь с таким email уже существует")
                return "not_unique_email"
            elif res2['count'] > 0:
                return "not_unique_username"
            self.__cursor.execute("INSERT INTO user VALUES(NULL, ?, ?, ?, ?, ?)", (username, email, pass_hash, gender,
                                                                                   is_confirmed))
            self.__db.commit()
        except sqlite3.Error as e:
            print(str(e))
            return False

        return True

    def getUser(self, user_id):
        try:
            self.__cursor.execute(f"SELECT * FROM user WHERE id = {user_id} LIMIT 1")
            res = self.__cursor.fetchone()
            if not res:
                print("Пользователя не нашлось")
                return False
            return res
        except sqlite3.Error as e:
            print(str(e))
        return False

    def getUserByUsername(self, username):
        try:
            self.__cursor.execute(f"SELECT * FROM user WHERE username = '{username}' LIMIT 1")
            res = self.__cursor.fetchone()
            if not res:
                print("Пользователя не нашлось")
                return False
            return res
        except sqlite3.Error as e:
            print(str(e))
        return False

    def getUserByEmail(self, email):
        try:
            self.__cursor.execute(f"SELECT * FROM user WHERE email = '{email}' LIMIT 1")
            res = self.__cursor.fetchone()
            if not res:
                print("Пользователя не нашлось")
                return False
            return res
        except sqlite3.Error as e:
            print(str(e))
        return False

    def confirmUserByEmail(self, email):
        try:
            conn = sqlite3.connect(r"C:\Users\Михаил\Desktop\flaskStudyingProject\app\flask_app.db")
            cur = conn.cursor()
            cur.execute(f"UPDATE user SET is_confirmed = 1 where email = '{email}'")
            conn.commit()
        except sqlite3.Error as e:
            print(str(e))
        return False

    def deleteUser(self, username):
        try:
            conn = sqlite3.connect(r"C:\Users\Михаил\Desktop\flaskStudyingProject\app\flask_app.db")
            cur = conn.cursor()
            cur.execute(f"DELETE FROM user where username = '{username}'")
            conn.commit()
        except sqlite3.Error as e:
            print(str(e))
        return False

    def editUser(self, field_to_change, new_value, username):
        try:
            conn = sqlite3.connect(r"C:\Users\Михаил\Desktop\flaskStudyingProject\app\flask_app.db")
            cur = conn.cursor()
            if field_to_change == 'is_confirmed' or field_to_change == 'role_id':
                cur.execute(f"UPDATE user SET {field_to_change} = {new_value} where username = '{username}'")
            else:
                cur.execute(f"UPDATE user SET {field_to_change} = '{new_value}' where username = '{username}'")
            conn.commit()
        except sqlite3.Error as e:
            print(str(e))
        return False