from flask_login import UserMixin


class UserLogin(UserMixin):

    def fromDB(self, user_id, db):
        self.__user = db.getUser(user_id)
        return self

    def create(self, user):
        self.__user = user
        return self

    def get_id(self):
        return str(self.__user['id'])

    def get_username(self):
        return str(self.__user['username'])

    def get_email(self):
        return str(self.__user['email'])

    def get_gender(self):
        return str(self.__user['gender'])

    def get_is_confirmed(self):
        return str(self.__user['is_confirmed'])

    def get_role_id(self):
        return str(self.__user['role_id'])
