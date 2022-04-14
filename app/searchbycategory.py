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
        year = None if request.form['year'] == "" else  request.form['year']
        author = None if request.form['author'] == "" else request.form['author'].strip()
        conference = None if request.form['conference'] == "" else request.form['conference'].strip()
        if year is not None: 
            try: 
                year = int(year)
            except: 
                flash("Year entered must be an valid integer")
                return render_template('searchbycategory.html')

        if  year is None and author is None and conference is None:
            error = "At least one category (year/ author/ conference) is required"
            flash(error)
            return render_template('searchbycategory.html')

        search_string = ""
        if year is not None and author is not None and conference is not None:
            search_string+="year##"+str(year)+"$$"+"author##"+author+"$$"+"conference##"+conference
        elif year is not None and author is not None:
            search_string+="year##"+str(year)+"$$"+"author##"+author+"$$"+"conference##"+"%%"
        elif year is not None and conference is not None:
            search_string+="year##"+str(year)+"$$"+"author##"+"%%"+"$$"+"conference##"+conference
        elif author is not None and conference is not None:
            search_string+="year##"+"%%"+"$$"+"author##"+author+"$$"+"conference##"+conference
        elif year is not None:
            search_string+="year##"+str(year)+"$$"+"author##"+"%%"+"$$"+"conference##"+"%%"
        elif author is not None:
            search_string+="year##"+"%%"+"$$"+"author##"+author+"$$"+"conference##"+"%%"
        else:
            search_string+="year##"+"%%"+"$$"+"author##"+"%%"+"$$"+"conference##"+conference

        return redirect(url_for("searchbycategory.search_by_category_view",search_string=search_string,pagenum=0))
    

@bp.route('/searchbycategory_view/<search_string>/<pagenum>', methods=('GET', 'POST'))
# year, author, conference
def search_by_category_view(search_string,pagenum):    
        pagenum = int(pagenum)
        cats = search_string.split("$$")
        year = None
        author = None
        conference = None 
        show_string= ""
        for cat in cats:
            cat_split = cat.split('##')
            cat_name=cat_split[0] 
            cat_content = cat_split[1]
            if cat_name =="year" and cat_content!="%%": 
                year = int(cat_content)
                show_string +="Year="+cat_content+"; "
            if cat_name =="author" and cat_content!="%%": 
                author = cat_content
                show_string +="Author="+cat_content+"; "
            if cat_name =="conference" and cat_content!="%%": 
                conference = cat_content
                show_string +="Conference="+cat_content+"; "
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
        if request.method == 'POST':
            pagenum = int(request.form['pagenum'])
            if not pagenum:
                pagenum = 0
        total_num =len(papers)
        if pagenum*10<total_num:
            if (pagenum+1)*10>total_num:
                    papers = papers[(pagenum*10):-1]
            papers= papers[(pagenum*10):(pagenum+1)*10]
        else: papers = []
        total_num = int(total_num/10)
        return render_template('searchbycategory_view.html', 
                            paper_list=papers,pagenum=pagenum,
                            total_num=total_num,
                            show_string= show_string)
    
