from flask import current_app as app


class Paper:
    def __init__(self, pid, title, year, conference):
        self.pid = pid
        self.title = title
        self.year = year
        self.conference = conference

    @staticmethod
    def get(pid):
        rows = app.db.execute(
            '''
            SELECT pid, title, year, conference
            FROM papers
            WHERE pid = :pid
            ''', pid=pid)
        return Paper(*(rows[0])) if rows is not None else None

    @staticmethod
    def get_paper_for_one_page(pagesize, pagenum):
        rows = app.db.execute(
            '''
            SELECT pid, title, year, conference
            FROM papers
            ORDER BY pid
            LIMIT :pagesize OFFSET :offset
            ''', pagesize=pagesize, offset=pagenum*pagesize)
        return [Paper(*row) for row in rows]
