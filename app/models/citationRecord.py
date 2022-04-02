from flask import current_app as app


class CitationRecord:
    def __init__(self, pid, cite_pid):
        self.pid = pid
        self.cite_pid = cite_pid
        #pid cite cite_pid

    @staticmethod
    def get_by_pid(pid):
        rows = app.db.execute(
            '''
            SELECT pid, cite_pid
            FROM citation
            WHERE cite_pid = :pid
            ''', pid=pid)
        return [CitationRecord(*row) for row in rows]
