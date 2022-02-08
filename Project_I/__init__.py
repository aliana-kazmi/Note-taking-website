from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

db = SQLAlchemy()
DB_NAME = "database.db"

#function for creation of database
def create_database(app):
    if not path.exists('website/' + DB_NAME):
        db.create_all(app = app)
        print('Database created successfully!')

 
def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'hello this string is very important. Dont share this with anyone'
    # we are telling flask where database is located
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)

    from .views import views
    from .auth import auth
    
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    
    from .models import User, Note 
    create_database(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(id)


    return app