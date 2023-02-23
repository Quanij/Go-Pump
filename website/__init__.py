from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

db = SQLAlchemy()
DB_NAME = "database.db"
DB_PATH = path.join(path.abspath(path.dirname(__file__)), '..', 'instance', DB_NAME)


def create_app():
    app = Flask(__name__, static_folder='static')
    app.config['SECRET_KEY'] = 'thisismysecretkey' 
    ## app.config['SQLALCHEMY_DATABASE_URI'] = F'sqlite:///{DB_NAME}' 
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_PATH}'
    db.init_app(app) 
    
    from .views import views
    from .auth import auth
    
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    
    from .models import User, Pressure
    
    create_database(app)
    
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)
    
    @login_manager.user_loader
    def load_uer(id):
        return User.query.get(int(id))
    
    return app

def create_database(app):
    if not path.exists('instance/' + DB_NAME):
        with app.app_context():
            db.create_all()
            print('Created Database!')
        