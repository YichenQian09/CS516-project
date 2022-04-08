from flask import render_template, redirect, url_for, flash, request, Blueprint

from app.collection import RemovePapersForm
from .models.citationcart import CitationCart
from flask_login import current_user


bp = Blueprint('citationcart', __name__)

@bp.route('/citationcart', methods=['GET', 'POST'])
def citationcart():
    if not current_user.is_authenticated:
        return redirect(url_for('users.login'))
    
    pagesize = 10
    pagenum = 0
    pid_strings = []

    if request.method == 'POST':
        pagesize = request.form.get('pagesize')
        pagenum = request.form.get('pagenum')
        pid_strings = request.form.getlist('remove[]')
        print("pid_strings: ", pid_strings)    
        
        pagesize = 10 if not pagesize else int(pagesize)
        pagenum = 0 if not pagenum else int(pagenum)

  
    pids=tuple(int(pid) for pid in pid_strings)
    print("pids: ", pids)

    if len(pids) > 0 and CitationCart.remove_paper_from_cart_in_batch(current_user.uid, pids):
        print("You removed papers in batch from cart")
        return redirect(url_for("citationcart.citationcart"))

    citationcartlist=CitationCart.get_onepage_citations_of_a_citation_cart(current_user.uid, pagesize, pagenum)

    return render_template('citationcart.html',
                           paper_list=citationcartlist,
                           pagesize=pagesize,
                           pagenum = pagenum,
                           )


@bp.route('/checkout', methods=['POST', 'GET'])
def checkout():
    flash("checkout successfully")
    return redirect(url_for('citationcart.citationcart')) 


@bp.route('/remove_papers/<pid>', methods=['GET', 'POST'])
def remove_paper_from_citationcart(pid):
    if not current_user.is_authenticated:
        return redirect(url_for('users.login'))
    if CitationCart.remove_paper_from_cart(current_user.uid, pid):
        print("you removed a paper from cart")
    return redirect(url_for('citationcart.citationcart')) 