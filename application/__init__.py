from flask import Flask

def create_app():
    app=Flask(__name__,instance_relative_config=True)
    app.config.from_pyfile('config.py',silent=True)
    
    #Register your blueprint
    return app

# To run file "flask --app application_name run --debug --host=host_name"