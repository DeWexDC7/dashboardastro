import os

class Config:
    #SQLALCHEMY_DATABASE_URI = os.getenv('localhost', 'postgresql://admin:admin@localhost:5433/radiusmain')
    SQLALCHEMY_DATABASE_URI = os.getenv('localhost', 'postgresql://postgres:admin@localhost:5433/inventorydb')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
