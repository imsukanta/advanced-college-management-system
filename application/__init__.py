from flask import Flask

def create_app():
    app=Flask(__name__,instance_relative_config=True)
    app.config.from_pyfile('config.py',silent=True)
    
    #Register your blueprint
    from application.blueprint import dashboard
    app.register_blueprint(dashboard.bp)
    return app

