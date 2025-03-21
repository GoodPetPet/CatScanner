
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from watchlist import db 

class User(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True) # key
    name = db.Column(db.String(70))
    username = db.Column(db.String(20))  # 用户名
    password_hash = db.Column(db.String(128))  # 密码散列值
    def set_password(self, password):  # 用来设置密码的方法，接受密码作为参数
        self.password_hash = generate_password_hash(password)  # 将生成的密码保持到对应字段

    def validate_password(self, password):  # 用于验证密码的方法，接受密码作为参数
        return check_password_hash(self.password_hash, password)  # 返回布尔值

class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(60)) # 电影标题
    year = db.Column(db.String(4))
