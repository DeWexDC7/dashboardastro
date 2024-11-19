import os

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv('localhost', 'postgresql://admin:admin@localhost/radiusmain')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
