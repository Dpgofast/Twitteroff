'''Main aplication and routing logic for Twitteroff'''
from flask import Flask
from .models import DB

def create_app():
    '''Create and configure an instance of an application.'''
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
    DB.init_app(app)


    @app.route('/')
    def root():
        return 'Welcome To Twitteroff (U+1F98B)'
   
    return app    