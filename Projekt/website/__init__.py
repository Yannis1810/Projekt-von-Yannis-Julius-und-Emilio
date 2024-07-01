from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

db = SQLAlchemy()
DB_NAME = "Projekt-Datenbank.db"


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'heheheha hahahahe'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)

    from .views import views # Pfade werden importiert (bspw. die Startseite)
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import User, Note, Repair # Tabellen der Datenbank werden importiert
    
    with app.app_context():
        db.create_all()

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login' # Seite auf der man sich anmeldet wird angegeben
    login_manager.init_app(app)

    @login_manager.user_loader # lädt den User anhand seiner ID
    def load_user(id):
        return User.query.get(int(id))

    return app


def create_database(app):
    if not path.exists('website/' + DB_NAME): # wenn die Datenbank noch  nicht existiert, wird sie hiermit erstellt (hierfür auch über das Betriebssystem die Pfade importiert)
        db.create_all(app=app)
        print('Created Database!')
    