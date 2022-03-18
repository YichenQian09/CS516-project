from flask import current_app as app


class Paper:
    def __init__(self, pid, title, year, conference):
        self.pid = pid
        self.title = title
        self.year = year
        self.conference = conference

    @staticmethod
    def get_by_pid(pid):
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

    @staticmethod
    def get_by_title(title):
        rows = app.db.execute(
            '''
            SELECT pid, title, year, conference
            FROM papers
            WHERE title = :title
            ORDER BY pid
            ''', title=title)
        return [Paper(*row) for row in rows]

    @staticmethod
    def get_by_year(year):
        rows = app.db.execute(
            '''
            SELECT pid, title, year, conference
            FROM papers
            WHERE year = :year
            ORDER BY pid
            ''', year=year)
        return [Paper(*row) for row in rows]
    
    @staticmethod
    def get_by_author(author):
        rows = app.db.execute(
            '''
            SELECT papers.pid, title, year, conference
            FROM papers 
            INNER JOIN
            (
                SELECT pid, author
                FROM authorship
                WHERE author = :author
            ) AS t1
            ON papers.pid = t1.pid
            ORDER BY papers.pid
            ''', author=author)
        return [Paper(*row) for row in rows]

    @staticmethod
    def get_by_conference(conference):
        rows = app.db.execute(
            '''
            SELECT pid, title, year, conference
            FROM papers
            WHERE conference = :conference
            ORDER BY pid
            ''', conference=conference)
        return [Paper(*row) for row in rows]

    @staticmethod
    def get_by_year_author_conf(year, author, conference):
        rows = app.db.execute(
            '''
            SELECT t1.pid, title, year, conference
            FROM 
            (
                SELECT pid, title, year, conference
                FROM papers
                WHERE year = :year AND conference = :conference
            ) AS t1
            INNER JOIN
            (
                SELECT pid, author
                FROM authorship
                WHERE author = :author
            ) AS t2
            ON t1.pid = t2.pid
            ORDER BY t1.pid
            ''', year=year, author=author, conference=conference)
        return [Paper(*row) for row in rows]
    
    @staticmethod
    def get_by_year_author(year, author):
        rows = app.db.execute(
            '''
            SELECT t1.pid, title, year, conference
            FROM 
            (
                SELECT pid, title, year, conference
                FROM papers
                WHERE year = :year
            ) AS t1
            INNER JOIN
            (
                SELECT pid, author
                FROM authorship
                WHERE author = :author
            ) AS t2
            ON t1.pid = t2.pid
            ORDER BY t1.pid
            ''', year=year, author=author)
        return [Paper(*row) for row in rows]

    @staticmethod
    def get_by_author_conf(author, conference):
        rows = app.db.execute(
            '''
            SELECT t1.pid, title, year, conference
            FROM 
            (
                SELECT pid, title, year, conference
                FROM papers
                WHERE conference = :conference
            ) AS t1
            INNER JOIN
            (
                SELECT pid, author
                FROM authorship
                WHERE author = :author
            ) AS t2
            ON t1.pid = t2.pid
            ORDER BY t1.pid
            ''', conference=conference, author=author)
        return [Paper(*row) for row in rows]


    @staticmethod
    def get_by_year_conf(year, conference):
        rows = app.db.execute(
            '''
            SELECT pid, title, year, conference
            FROM papers
            WHERE year = :year AND conference = :conference
            ORDER BY pid
            ''', year=year, conference=conference)
        return [Paper(*row) for row in rows]