import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite:///" + os.path.join(basedir, "reservas.db"))
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    GERENCIAMENTO_BASE_URL = os.getenv("GERENCIAMENTO_BASE_URL", "http://gerenciamento:5000") 