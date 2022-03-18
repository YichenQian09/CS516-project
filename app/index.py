<<<<<<< HEAD
from flask import render_template
from flask_login import current_user
import datetime

=======
from crypt import methods
import re
from flask import render_template, request
from flask_login import current_user
import datetime

from .models.product import Product
from .models.purchase import Purchase
from .models.paper import Paper

>>>>>>> origin/zx_dev
from flask import Blueprint
bp = Blueprint('index', __name__)


<<<<<<< HEAD
@bp.route('/')
def index():
    # render the page by adding information to the index.html file
    return render_template('index.html')
=======
# @bp.route('/')
# def index():
#     # get all available products for sale:
#     products = Product.get_all(True)
#     # find the products current user has bought:
#     if current_user.is_authenticated:
#         purchases = Purchase.get_all_by_uid_since(
#             current_user.id, datetime.datetime(1980, 9, 14, 0, 0, 0))
#     else:
#         purchases = None
#     # render the page by adding information to the index.html file
#     return render_template('index.html',
#                            avail_products=products,
#                            purchase_history=purchases)

@bp.route('/', methods=('GET', 'POST'))
def index():
    return render_template('home.html')
>>>>>>> origin/zx_dev
