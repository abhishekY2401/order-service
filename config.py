import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    DB_PASSWORD = os.environ['DB_PASSWORD']
    RABBITMQ_URL = os.environ['RABBITMQ_URI']
    SQLALCHEMY_DATABASE_URI = (
        f'postgresql://postgres:{DB_PASSWORD}@localhost:5432/orders_db'
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.environ['JWT_SECRET_KEY']
    ORDER_PLACED_QUEUE = "order.placed"
    ORDER_SHIPPED_QUEUE = "order.shipped"


class DevelopmentConfig(Config):
    DEBUG = True


class ProductionConfig(Config):
    DEBUG = False
