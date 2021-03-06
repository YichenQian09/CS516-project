from flask import render_template, request, Blueprint, flash
from .models.paper import Paper
bp = Blueprint('paperindex', __name__)


@bp.route('/papers', methods=('GET', 'POST'))
@bp.route('/<int:pagesize>/<int:pagenum>/papers', methods=('GET', 'POST'))
def paperindex(pagesize = 10, pagenum = 0):
    if request.method == 'POST':
        try:
            pagesize = int(request.form['pagesize'])
            pagenum = int(request.form['pagenum'])
        except: 
            flash("Page size and Page number input must be valid integers")
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
