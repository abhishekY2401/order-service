import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    RABBITMQ_URL = os.environ['RABBITMQ_URI']
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.environ['JWT_SECRET_KEY']
    ORDER_PLACED_QUEUE = "order.placed"
    ORDER_SHIPPED_QUEUE = "order.shipped"


class DevelopmentConfig(Config):
    DEBUG = True


class ProductionConfig(Config):
    DEBUG = False
