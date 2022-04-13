from flask import current_app as app

class Orderinfo:
    def __init__(self, order_num, citenum_of_this_order):
        self.order_num = order_num
        self.citenum_of_this_order = citenum_of_this_order  

    @staticmethod
    def get_citation_order(uid):
        rows = app.db.execute(
            '''
            SELECT order_num, count(*) as citenum_of_this_order
            FROM Users_cite_history
            WHERE uid = :uid
            GROUP BY order_num
            '''
        , uid = uid)
        return [Orderinfo(*row) for row in rows]