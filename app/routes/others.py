from flask import Blueprint, render_template
from datetime import datetime

other = Blueprint('other', __name__)

@other.route('/how')
def how():
    return render_template('abouthus/how.html')

@other.route('/team')
def team():
    return render_template('abouthus/team.html')

@other.route('/about')
def about():
    return render_template('abouthus/about.html')

from datetime import datetime

@other.context_processor
def inject_current_year():
    return {'current_year': datetime.utcnow().year}