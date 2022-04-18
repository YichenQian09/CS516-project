from crypt import methods
import re
from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from flask_login import current_user

from .models.paper import Paper

from flask import Blueprint
bp = Blueprint('searchbycategory', __name__)


@bp.route('/searchbycategory', methods=('GET', 'POST'))
# year, author, conference
def search_by_category():
    if request.method == 'GET':
        return render_template('searchbycategory.html')
    
    if request.method == 'POST':
        # check TYPE! 
        year = None if request.form['year'] == "" else int (request.form['year'])
        author = None if request.form['author'] == "" else request.form['author'].strip()
        conference = None if request.form['conference'] == "" else request.form['conference'].strip()

        error = None

        
        if  year is None and author is None and conference is None:
            error = "At least one category (year/ author/ conference) is required"
        
        if error is not None:
            flash(error)
        
        papers = None
        if year is not None and author is not None and conference is not None:
            papers = Paper.get_by_year_author_conf(year, author, conference)
        elif year is not None and author is not None:
            papers = Paper.get_by_year_author(year, author)
        elif year is not None and conference is not None:
            papers = Paper.get_by_year_conf(year, conference)
        elif author is not None and conference is not None:
            papers = Paper.get_by_author_conf(author, conference)
        elif year is not None:
            papers = Paper.get_by_year(year)
        elif author is not None:
            papers = Paper.get_by_author(author)
        else:
            papers = Paper.get_by_conference(conference)

        return render_template('searchbycategory.html', paper_list=papers)
    
