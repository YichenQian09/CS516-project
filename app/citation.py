from flask import render_template, url_for, redirect, Blueprint
from flask_login import current_user

from .models.citations import Citations

bp = Blueprint('citation', __name__)

@bp.route('/citation_history', methods=['GET'])
def get_citation_history():
    if not current_user.is_authenticated:
        return redirect(url_for('users.login'))
    citation_history = Citations.get_citations(current_user.uid)
    print ("citation_history", citation_history)
    return render_template('citationhistory.html', paper_list=citation_history)
