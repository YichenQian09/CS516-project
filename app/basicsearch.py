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
            flash(error)
            return redirect(url_for("basicsearch.basic_search"))
        
        if pid is not None and title is None:
            if not isinstance(pid, int):
                flash("pid entered must be integers")
                return redirect(url_for("basicsearch.basic_search"))
            return redirect(url_for("basicsearch.basic_search_view_pid", pid = pid, pagenum=0))
        elif pid is None and title is not None:
            return redirect(url_for("basicsearch.basic_search_view_title",title=title,pagenum=0))
        else: 
            if not isinstance(pid, int):
                flash("pid entered must be integers")
                return redirect(url_for("basicsearch.basic_search"))
            flash("Using paper id as the primary identifier")
            return redirect(url_for("basicsearch.basic_search_view_pid", pid = pid, pagenum=0))
        
@bp.route('/basicsearch_pid/<pid>/<pagenum>',methods=('GET', 'POST'))
def basic_search_view_pid(pid,pagenum):
    pagenum = int(pagenum)
    papers = Paper.get_by_pid(pid)
    total_num = 0
    return render_template('basicsearch_view.html', 
                        paper_list=papers, 
                        pagenum=pagenum, 
                        total_num=total_num, 
                        search_pid=pid)
                        
@bp.route('/basicsearch_title/<title>/<pagenum>', methods=('GET', 'POST'))
def basic_search_view_title(title,pagenum):
    pagenum = int(pagenum)
    if request.method == 'POST':
        pagenum = int(request.form['pagenum'])
        if not pagenum:
            pagenum = 0
    papers,total_num = Paper.get_by_title(title,pagenum)
    total_num = int(total_num/10)
    return render_template('basicsearch_view.html', 
                        paper_list=papers, 
                        pagenum=pagenum, 
                        total_num=total_num, 
                        search_pid=None, 
                        search_title=title)

