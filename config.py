from datetime import timedelta
import os
from dotenv import load_dotenv

load_dotenv()  

def configure_app(app):
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
    app.config['HOST'] = '0.0.0.0'
    app.config['PORT'] = 5000
    app.config['DEBUG'] = True
    expires_seconds = int(os.getenv('JWT_EXPIRES', 7200))
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(seconds=expires_seconds)
