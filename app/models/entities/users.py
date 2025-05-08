from flask_login import UserMixin

class User(UserMixin):
    def __init__(self, id, email, password, usertype, fullname="" ) -> None:
        self.id = id
        self.email = email
        self.password = password
        self.fullname = fullname
        self.usertype = usertype