from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from flask_migrate import Migrate
class Base(DeclarativeBase):
    pass
db=SQLAlchemy(model_class=Base)
def create_app():
    app=Flask(__name__,instance_relative_config=True)
    app.config.from_pyfile('config.py',silent=True)
    app.config['SQLALCHEMY_DATABASE_URI']= "sqlite:///project.db"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
    db.init_app(app)
    #import all models here
    Migrate(app,db)
    from application.models import department
    #Register your blueprint
    return app

# To run file "flask --app application_name run --debug --host=host_name"