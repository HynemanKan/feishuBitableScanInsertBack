from flask_login import UserMixin


class Account(UserMixin):
    user_id:str
    access_token:str
