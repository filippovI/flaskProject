from app import db, Users


class AddAdmin:
    def __init__(self, login: str, password: str, admin: bool = False):
        self.login = login
        self.password = str(password)
        self.admin = admin

    def add(self) -> str:
        users = Users(login=self.login,
                      password=self.password,
                      admin=str(self.admin))

        try:
            db.session.add(users)
            db.session.commit()
            return f'Пользователь {self.login} успешно добавлен'
        except(Exception,) as err:
            return f'Ошибка добавления пользователя {err}'