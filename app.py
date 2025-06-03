from flask import Flask
from flask_jwt_extended import JWTManager
from config import configure_app
from routes.AuthRoutes import auth_bp
from routes.Home import home
from routes.ResultsRoutes import resultados_bp
from flask_migrate import Migrate
from extensios import db

app = Flask(__name__)
configure_app(app)


db.init_app(app)

with app.app_context():
    db.create_all()
    print("Database tables created successfully.")

migrate = Migrate(app, db)


jwt = JWTManager(app)

app.register_blueprint(auth_bp)
app.register_blueprint(home)
app.register_blueprint(resultados_bp)

if __name__ == '__main__':
    app.run(
        host=app.config['HOST'],
        port=app.config['PORT'],
        debug=app.config['DEBUG']
    )
