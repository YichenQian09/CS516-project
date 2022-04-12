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
from .models.comment import Comment
from .models.comment import Helpful
from .models.users import Users


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
      
    comments=Comment.fetch_comment_by_pid(pid)
    comment_exist =  Comment.check_if_commented_by_pid_uid(pid,current_user.uid)
    sum_score, num_score = Comment.get_average_star(pid)
    not_upvoted_by=[]
    username = []
    for com in comments:
        not_upvoted_by.append(not (Helpful.check_if_upvoted(com.pid,com.uid,current_user.uid)))
        username.append(Users.get_profile(com.uid).nickname)
    print(not_upvoted_by)
    return render_template('paperinfopage.html', 
                            paper=paper[0], 
                            abstract=abstract, 
                            authors = authors, 
                            citing_papers = citing_papers,
                            cited_list=cited_list,
                            collection_choices = choices,
                            collect_form = collect_form,
                            comments = comments,
                            comment_num = len(comments),
                            comment_exist = comment_exist,
                            sum_score = sum_score,
                            num_score = num_score,
                            not_upvoted_by=not_upvoted_by,
                            username = username)

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
        
    full_url = url_for('paperinfo.get_paper_info',pid=pid)
    return redirect(full_url)

@bp.route('/submit_message/<pid>', methods=['POST'])
def submit_message(pid):
    if not current_user.is_authenticated:
        return redirect(url_for('users.login'))
    comment_sum = request.form.get("comment_summary")
    comment = request.form.get("comment")
    star = int(request.form.get("star"))
    print("star:",star,type(star))
    uid = current_user.uid
    if not Comment.check_if_commented_by_pid_uid(pid,uid): 
        if Comment.add_comment(pid,uid,star,comment_sum,comment,0):
            print("Comment added successfully")
        else: flash("Something went wrong!Please re-submit your comment") #This should never happen
    return redirect(url_for('paperinfo.get_paper_info',pid=pid))


@bp.route('/paperinfo/upvote/<pid>/<uid>', methods=('GET','POST'))
def upvote_comment(pid,uid):
    if not current_user.is_authenticated:
        return redirect(url_for('users.login'))
    if not Helpful.check_if_upvoted(pid,uid,current_user.uid): 
        Helpful.upvote_comment(pid,uid,current_user.uid)
        Comment.upvote_comment(pid,uid)
    return redirect(url_for('paperinfo.get_paper_info',pid=pid))

@bp.route('/paperinfo/cancel/<pid>/<uid>', methods=('GET','POST'))
def cancel_upvote(pid,uid):
    if not current_user.is_authenticated:
        return redirect(url_for('users.login'))
    if Helpful.check_if_upvoted(pid,uid,current_user.uid): 
        Helpful.cancel_upvote(pid,uid,current_user.uid)
        Comment.cancel_upvote(pid,uid)
    return redirect(url_for('paperinfo.get_paper_info',pid=pid))

        



# @bp.route("/pick_collection")
# def input():
#     choices = Collections.get_each_collection_name(current_user.uid)
#     return redirect(url_for('paperinfo.paperinfo'))

