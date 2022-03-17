from crypt import methods
import re
from flask import render_template, request
from flask_login import current_user
import datetime

from .models.product import Product
from .models.purchase import Purchase
from .models.paper import Paper

from flask import Blueprint
bp = Blueprint('paperindex', __name__)


@bp.route('/papers', methods=('GET', 'POST'))
@bp.route('/<int:pagesize>/<int:pagenum>/papers', methods=('GET', 'POST'))
def paperindex(pagesize = 10, pagenum = 0):
    if request.method == 'POST':
        pagesize = int(request.form['pagesize'])
        pagenum = int(request.form['pagenum'])
        
        if not pagesize:
            pagesize = 10
        if not pagenum:
            pagenum = 0

    # get current $pagesize (e.g., 100) papers on current $pagenum
    papers = Paper.get_paper_for_one_page(pagesize, pagenum)
    
    # render the page by adding information to the paperindex.html file
    return render_template('paperlist.html',
                           paper_list=papers,
                           pagesize=pagesize,
                           pagenum = pagenum
                           )