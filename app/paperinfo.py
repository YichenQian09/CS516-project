from crypt import methods
from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from flask_login import current_user
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import ValidationError, DataRequired

from .models.paper import Paper, Authors, Abstract
from .models.browses import Browses
from .models.citationRecord import CitationRecord
from .models.citationcart import CitationCart
from .models.collections import Collections

class CitePaper(FlaskForm):
    submit = SubmitField('Cite')
    def check_if_paper_in_cart(self, uid, pid):
        if CitationCart.check_if_already_in_cart(uid, pid):
            raise ValidationError('This paper is already in cart')

class LikePaper(FlaskForm):
    submit = SubmitField('Like')

class CollectPaper(FlaskForm):
    submit = SubmitField('Collect')

bp = Blueprint('paperinfo', __name__)


@bp.route('/paperinfo',methods=('GET', 'POST'))
# search by title or pid
def get_paper_info():
    if not current_user.is_authenticated:
        return redirect(url_for('users.login'))
    args = request.args
    pid = args.get("pid")

    error = None

    if pid is None:
        error = "miss query parameter"
    
    if error is not None:
        flash(error)
    
    pid = int(pid)
    paper = Paper.get_by_pid(pid)
    abstract = Abstract.get_by_pid(pid)
    authors = Authors.get_by_pid(pid)
    citing_papers = Paper.get_citing_papers_by_pid(pid)
    cited_list = CitationRecord.get_by_pid(pid)
    
    # so it will record the browse history when the user click
    record=Browses.record_browse(current_user.uid,pid)
    choices = Collections.get_each_collection_name(current_user.uid)
    
    # collect paper into collections other than 'Liked'
    collect_form = CollectPaper()
    if collect_form.validate_on_submit():
        collection_name_selected= request.form.get("Collection")
        print("value:",collection_name_selected)
        if Collections.check_paper_in_collection(current_user.uid,collection_name_selected,pid):
            flash("Collected already! ")
        else:
            Collections.add_paper_in_collection(current_user.uid,collection_name_selected,pid)
            flash("You added a paper to "+collection_name_selected+" ! ")
      

    return render_template('paperinfopage.html', 
                            paper=paper[0], 
                            abstract=abstract, 
                            authors = authors, 
                            citing_papers = citing_papers,
                            cited_list=cited_list,
                            collection_choices = choices,
                            collect_form = collect_form)
                    



@bp.route('/paperinfo/like/<pid>',methods=('GET', 'POST'))
def like_paper(pid):
    if not current_user.is_authenticated:
        return redirect(url_for('users.login'))
    if Collections.check_paper_in_collection(current_user.uid,'Liked',pid):
        flash("Liked already! ")
    else: 
        Collections.add_paper_in_collection(current_user.uid,'Liked',pid)
        flash("You added a paper to Liked! ")
        
    full_url = url_for('paperinfo.get_paper_info')+"?pid="+str(pid)
    return redirect(full_url)

@bp.route('/paperinfo/cite/<pid>',methods=('GET', 'POST'))
def cite_paper(pid):
    if not current_user.is_authenticated:
        return redirect(url_for('users.login'))
    if CitationCart.check_if_already_in_cart(current_user.uid,pid):
        flash("Already in Cart! ")
    else: 
        CitationCart.add_paper_to_cart(current_user.uid,pid)
        flash("You added a paper to cart! ")
        
    full_url = url_for('paperinfo.get_paper_info')+"?pid="+str(pid)
    return redirect(full_url)

# @bp.route("/pick_collection")
# def input():
#     choices = Collections.get_each_collection_name(current_user.uid)
#     return redirect(url_for('paperinfo.paperinfo'))

