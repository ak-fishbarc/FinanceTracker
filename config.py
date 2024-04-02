import os


class Config:
    SECRET_KEY = os.environ.get('PROJECT_KEY')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
