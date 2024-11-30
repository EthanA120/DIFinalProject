import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = "slkjfnvajhtvnlkjdhrtgvlksd"
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{os.path.join(basedir, 'games.db')}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    MAIL_SERVER = "smtp.gmail.com"
    MAIL_PORT = 465
    MAIL_USERNAME = "ethanam120@gmail.com"
    MAIL_PASSWORD = "kxpu poxx satt kazx" # Password created by Google
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True