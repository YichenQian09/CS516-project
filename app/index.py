from crypt import methods
import re
from flask import render_template, request
from flask_login import current_user
import datetime

from .models.purchase import Purchase
from .models.paper import Paper

from flask import Blueprint
bp = Blueprint('index', __name__)

@bp.route('/', methods=('GET', 'POST'))
def index():
    return render_template('home.html')
#################################