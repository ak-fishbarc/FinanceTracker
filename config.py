import os


class Config:
    SECRET_KEY = os.environ.get('PROJECT_KEY')
