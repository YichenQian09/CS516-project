from crypt import methods
import re
from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from flask_login import current_user

from .models.paper import Paper

from flask import Blueprint
bp = Blueprint('basicsearch', __name__)


@bp.route('/basicsearch', methods=('GET', 'POST'))
# search by title or pid
def basic_search():
    if request.method == 'GET':
        return render_template('basicsearch.html')
    
    if request.method == 'POST':
        pid = None if request.form['pid'] == "" else int (request.form['pid'])
        title = None if request.form['title'] == "" else request.form['title'].strip()
    
        error = None
        
        if  pid is None and title is None:
            error = "At least one identifier (paper id or title) is required"
        
        if error is not None:
            flash(error)
        
        papers = None
        if pid is not None and title is None:
            papers = Paper.get_by_pid(pid)
        elif pid is None and title is not None:
            papers = Paper.get_by_title(title)
        else:
            flask("Using paper id as the primary identifier")
            papers = Paper.get_by_pid(pid)

        return render_template('basicsearch.html', paper_list=papers)
    

