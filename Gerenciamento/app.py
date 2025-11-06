from flask import Flask
from flasgger import Swagger
from controller.route import setup_routes
from models.database import db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'projeto-API'

swagger = Swagger(app)
db.init_app(app)
setup_routes(app)

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)