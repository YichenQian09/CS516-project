from crypt import methods
import re
from flask import render_template, request
from flask_login import current_user
import datetime


from .models.paper import Statistic

from flask import Blueprint
bp = Blueprint('index', __name__)

@bp.route('/', methods=('GET', 'POST'))
def index():
    #author_sta = Statistic.get_author_statistic()
    #year_sta = Statistic.get_year_statistic()
    return render_template('home.html')
#################################