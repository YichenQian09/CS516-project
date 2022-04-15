from datetime import datetime
from app.models.paper import Paper
from flask import render_template, redirect, url_for, flash, request, Blueprint
from sqlalchemy import null

from app.collection import RemovePapersForm
from .models.citationcart import CitationCart, PaperFull
from .models.usercitation import Usercitation
from .models.users import Users
from flask_login import current_user


bp = Blueprint('citationcart', __name__)

@bp.route('/citationcart', methods=['GET', 'POST'])
def citationcart():
    if not current_user.is_authenticated:
        return redirect(url_for('users.login'))
    
    pagesize = 10
    pagenum = 0
    pid_strings = []
    currAction = None 

    if "action" in request.form:
        currAction = request.form.get("action")

    if request.method == 'POST':
        pagesize = request.form.get('pagesize')
        pagenum = request.form.get('pagenum')
        pid_strings = request.form.getlist('remove[]')
        
        pagesize = 10 if not pagesize else int(pagesize)
        pagenum = 0 if not pagenum else int(pagenum)

    if currAction =="Checkout cart":
        cited_papers = CitationCart.get_all_citations_of_a_citation_cart(current_user.uid)
        pids = [paper.pid for paper in cited_papers]
        pids_string = [str(paper.pid) for paper in cited_papers]
        pids_str = "#".join(pids_string)
        CitationCart.empty_cart(current_user.uid)
        ordernum = datetime.now()
        Usercitation.add_to_usercitation(current_user.uid, ordernum, pids)
        add_citenum = len(pids)
        Users.update_citenum(add_citenum,current_user.uid)
        return redirect(url_for("citationcart.checkout_successfully",pids=pids_str,ordernum = ordernum))
    else: 
        pids=tuple(int(pid) for pid in pid_strings)
        pids_str = "#".join(pid_strings)


        if len(pids) > 0:
            CitationCart.remove_paper_from_cart_in_batch(current_user.uid, pids)
            if currAction=="Checkout selected paper":
                ordernum = datetime.now()
                Usercitation.add_to_usercitation(current_user.uid, ordernum, pids)
                add_citenum = len(pids)
                Users.update_citenum(add_citenum, current_user.uid)
                return redirect(url_for("citationcart.checkout_successfully",pids=pids_str,ordernum=ordernum))

            return redirect(url_for("citationcart.citationcart"))

    citationcartlist=CitationCart.get_onepage_citations_of_a_citation_cart(current_user.uid, pagesize, pagenum)

    return render_template('citationcart.html',
                           paper_list=citationcartlist,
                           pagesize=pagesize,
                           pagenum = pagenum,
                           )

@bp.route('/checkout_successfully/<pids>/<ordernum>',methods=['GET', 'POST'])
def checkout_successfully(pids,ordernum):
    pids = [int(pid) for pid in pids.split("#")]
    checkout_paper=[]
    for pid in pids: 
        checkout_paper.append(PaperFull.get_full_info_by_pid(pid))
    checkout_paper.sort()
    ref_str = ""
    for paper in checkout_paper: 
        if paper.authors=="":
            paper_str = paper.title+". ("+str(paper.year)+"). "+paper.conference+".\n"
        else:
            if paper.conference is not None: 
                paper_str = paper.authors+" ("+str(paper.year)+"). "+paper.title+". "+paper.conference+".\n"
            else: paper_str = paper.authors+" ("+str(paper.year)+"). "+paper.title+".\n"
        ref_str +=paper_str
    return render_template("checkout_success.html",checkout_paper = checkout_paper, ref_str = ref_str,ordernum=ordernum)

@bp.route('/remove_papers/<pid>', methods=['GET', 'POST'])
def remove_paper_from_citationcart(pid):
    if not current_user.is_authenticated:
        return redirect(url_for('users.login'))
    if CitationCart.remove_paper_from_cart(current_user.uid, pid):
        flash("you removed a paper from cart")
    return redirect(url_for('citationcart.citationcart')) 
