from flask import render_template, redirect, url_for, flash, request
from flask_login import current_user
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import ValidationError, DataRequired


from .models.browses import Browses

from flask import Blueprint

bp = Blueprint('browse', __name__)

@bp.route('/get_browse_papers/<timerange>', methods=['GET', 'POST'])
def get_browse_papers(timerange):
    if not current_user.is_authenticated:
        return redirect(url_for('users.login'))
    # the function returns a list of tuples
    # (collection_name, numbers of papers)
    paper_list=Browses.get_papers(current_user.uid,timerange)
    return render_template('browsedpaper.html', title='Browsedpaper', paper_list=paper_list,timerange=timerange)

@bp.route('/record_browse', methods=['GET', 'POST'])
def record_browse():
    if not current_user.is_authenticated:
        return redirect(url_for('users.login'))
    # the function returns a list of tuples
    # (collection_name, numbers of papers)
    record=Browses.record_browse(current_user.uid,45)
    print("record:",record)  
    return redirect(url_for('index.index'))
