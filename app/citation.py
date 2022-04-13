from flask import render_template, url_for, redirect, Blueprint
from flask_login import current_user

from .models.citations import Citations
from .models.orderinfo import Orderinfo

bp = Blueprint('citation', __name__)

@bp.route('/citation_history', methods=['GET'])
def get_citation_history():
    if not current_user.is_authenticated:
        return redirect(url_for('users.login'))
    citation_history = Citations.get_citations(current_user.uid)
    print ("citation_history", citation_history)
    return render_template('citationhistory.html', paper_list=citation_history)

@bp.route('/citation_order', methods=['GET'])
def get_citation_orders():
    if not current_user.is_authenticated:
        return redirect(url_for('users.login'))
    citation_order = Orderinfo.get_citation_order(current_user.uid)
    print("citation order", citation_order)
    return render_template('orderhistory.html', order_history = citation_order)

@bp.route('/citation_history_by_order/<order_num>', methods=['GET'])
def get_citation_history_by_order(order_num):
    if not current_user.is_authenticated:
        return redirect(url_for('users.login'))
    citation_history_by_order = Citations.get_citations_by_order(current_user.uid, order_num)
    print ("citation_history_by_order", citation_history_by_order)
    return render_template('citationhistory.html', paper_list=citation_history_by_order)

