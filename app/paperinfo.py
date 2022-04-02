from crypt import methods
import re
from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from flask_login import current_user

from .models.paper import Paper
from .models.abstract import Abstract
from .models.browses import Browses
from .models.citationRecord import CitationRecord
from .models.authors import Authors


from flask import Blueprint
bp = Blueprint('paperinfo', __name__)


@bp.route('/paperinfo',methods=('GET', 'POST'))
# search by title or pid
def get_paper_info():
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
    
    return render_template('paperinfopage.html', 
                            paper=paper[0], 
                            abstract=abstract, 
                            authors = authors, 
                            citing_papers = citing_papers,
                            cited_list=cited_list)
                    


