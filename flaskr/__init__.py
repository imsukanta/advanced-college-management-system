from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from flask_wtf.csrf import CSRFProtect
from flask_mail import Mail
from flask_migrate import Migrate
csrf=CSRFProtect()
mail = Mail()
class Base(DeclarativeBase):
    pass
db=SQLAlchemy(model_class=Base)
migrate = Migrate()
def create_app():
    app=Flask(__name__,instance_relative_config=True)
    app.config.from_pyfile("config.py",silent=True)
    # app.config['SQLALCHEMY_DATABASE_URI']="sqlite:///college_db.db"
    app.config['SQLALCHEMY_DATABASE_URI']="mysql+pymysql://root:@localhost/college_db"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
    #For gmail
    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USERNAME'] = "collgemanagamentsystem@gmail.com"
    app.config['MAIL_PASSWORD'] = "odhh ybtg jpgm odyg"
    app.config['MAIL_DEFAULT_SENDER'] = "collgemanagamentsystem@gmail.com"
    mail.init_app(app)
    csrf.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)
    #register all models here
    from flaskr import models
    # import flaskr.create_role
    # with app.app_context():
    #     db.create_all()
    from . import index
    from . import student
    from . import login
    from . import user
    from . import dept
    from . import staff
    from . import studentIndex
    from . import sessionyear
    from . import student_login
    from . import teacher_login
    from . import teacher_dashboard
    from . import course
    from . import enrollment
    from . import schedule
    from . import search
    from . import exam
    from . import role
    from flaskr.commands import register_commands
    app.register_blueprint(role.bp)
    app.register_blueprint(exam.bp)
    app.register_blueprint(search.bp)
    app.register_blueprint(schedule.bp)
    app.register_blueprint(enrollment.bp)
    app.register_blueprint(course.bp)
    app.register_blueprint(teacher_dashboard.bp)
    app.register_blueprint(teacher_login.bp)
    app.register_blueprint(dept.bp)
    app.register_blueprint(index.bp)
    app.register_blueprint(login.bp)
    app.register_blueprint(student.bp)
    app.register_blueprint(user.bp)
    app.register_blueprint(staff.bp)
    app.register_blueprint(studentIndex.bp)
    app.register_blueprint(sessionyear.bp)
    app.register_blueprint(student_login.bp)
    register_commands(app)
    return app