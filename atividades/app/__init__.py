from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flasgger import Swagger
from config import Config

db = SQLAlchemy()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    Swagger(app)

    from app.routes.atividade_routes import atividade_bp
    app.register_blueprint(atividade_bp)
    
    from app.routes.nota_routes import nota_bp
    app.register_blueprint(nota_bp)

    return app