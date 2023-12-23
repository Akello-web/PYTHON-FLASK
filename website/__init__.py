from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

#our database
db = SQLAlchemy()
DB_NAME = "myprojectdb.db"


def create_app():
    #name
    app = Flask(__name__)
    # Sets a secret key for the Flask app.
    app.config['SECRET_KEY'] = 'hjshjhdjah kjshkjdhjs'
    #Configures the SQLAlchemy database URI for the app
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    #Initializes the SQLAlchemy database extension (db) for the Flask app. 
    db.init_app(app)

    from .views import views
    from .auth import auth

#Registers a blueprint named views within the Flask app. 
    app.register_blueprint(views, url_prefix='/')
#Registers another
    app.register_blueprint(auth, url_prefix='/')

    from .models import User
    
    with app.app_context():
        db.create_all()

#Creates an instance of Flask-Login's 
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app


def create_database(app):
    #Checks if the database file doesn't exist in the specified location. I
    if not path.exists('website/' + DB_NAME):
        db.create_all(app=app)
        print('Created Database!')
