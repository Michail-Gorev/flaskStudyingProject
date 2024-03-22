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

    def addUser(self, username, email, pass_hash, gender):
        try:
            self.__cursor.execute(f"SELECT COUNT() as `count` FROM user WHERE email LIKE '{email}'")
            res = self.__cursor.fetchone()
            if res['count'] > 0:
                print("Пользователь с таким email уже сущесвтует")
                return False

            self.__cursor.execute("INSERT INTO user VALUES(NULL, ?, ?, ?, ?)", (username, email, pass_hash, gender))
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
