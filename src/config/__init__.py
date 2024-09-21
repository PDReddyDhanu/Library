import os

class Config:
    DEBUG = True
    TESTING = False
    SECRET_KEY = os.environ.get('SECRET_KEY', 'my_secret_key')
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://vjit:Str0ngP@ssw0rd!@161.97.186.196:9321/vjit'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    @staticmethod
    def init_app(app):
        pass