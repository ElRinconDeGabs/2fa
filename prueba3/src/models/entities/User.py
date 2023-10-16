from werkzeug.security import check_password_hash
from flask_login import UserMixin

class User(UserMixin):

    def __init__(self, id, username, password, fullname="", token="", token_timestamp=None) -> None:
        self.id = id
        self.username = username
        self.password = password
        self.fullname = fullname
        self.token = token
        self.token_timestamp = token_timestamp

    @classmethod
    def check_password(cls, hashed_password, password):
        return check_password_hash(hashed_password, password)
