from flask import current_app as app
from .paper import Paper
from .collections import Collections

class CitationCart:
    def __init__(self, uid, cite_pid, time_added):
        self.uid = uid
        self.cite_pid = cite_pid
        self.time_added=time_added
    
    @staticmethod
    def get_each_citation_cart(uid):
        #Returns a list of papers
        rows=app.db.execute(
            '''
            SELECT User_cart.cite_pid AS pid, Papers.title as title, Papers.year as year, Papers.conference as conference
            FROM User_cart JOIN Papers
            WHERE User_cart.uid = :uid AND User_cart.cite_pid=Papers.pid
            ''', uid=uid)
        return [Paper(*row) for row in rows]
