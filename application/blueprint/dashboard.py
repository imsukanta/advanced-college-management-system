from flask import Blueprint 
bp = Blueprint('dashboard', __name__, url_prefix='/dashboard') 


@bp.route('/')
def dashboard():
    return('hi')
