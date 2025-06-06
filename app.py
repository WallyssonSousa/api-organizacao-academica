from flask import Flask
from flask_jwt_extended import JWTManager
from config import configure_app
from routes.AuthRoutes import auth_bp
from routes.Home import home
from routes.ResultsRoutes import resultados_bp
from flask_migrate import Migrate
from extensios import db
from sqlalchemy.exc import OperationalError
import time

jwt = JWTManager()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    configure_app(app)
    db.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)

    app.register_blueprint(auth_bp)
    app.register_blueprint(home)
    app.register_blueprint(resultados_bp)

    with app.app_context():
        for _ in range(10):
            try:
                db.create_all()
                break
            except OperationalError:
                print("MySQL ainda não está pronto. Tentando novamente em 2s...")
                time.sleep(2)
        else:
            print("Erro: Banco não respondeu.")
            exit(1)

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(
        host=app.config['HOST'],
        port=app.config['PORT'],
        debug=app.config['DEBUG']
    )
