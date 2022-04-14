from flask import current_app as app
from wtforms import StringField, SubmitField
from flask_wtf import FlaskForm
from wtforms.validators import ValidationError, DataRequired

# CONTAINS CLASS:
# Paper
# Authors
# Abstract

class Paper:
    def __init__(self, pid, title, year, conference):
        self.pid = pid
        self.title = title
        self.year = year
        self.conference = conference

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
    
    @staticmethod
    def get_by_pid(pid):
        # (pid<=maximum pid) is checked before executing
        rows = app.db.execute(
            '''
            SELECT *
            FROM papers 
            WHERE pid = :pid
            ''', pid=pid)
        return [Paper(*rows[0])]
    
    @staticmethod
    def get_by_title(title_input,pagenum):
        pagenum = int(pagenum)
        sql_str = "SELECT papers.pid, title, year, conference FROM papers WHERE title LIKE '%"+title_input+"%' ORDER BY pid"
        rows = app.db.execute(sql_str)
        total_num = len(rows)
        if (pagenum+1)*10>total_num: 
            rows = rows[(pagenum*10):-1]
        rows = rows[(pagenum*10):((pagenum+1)*10)]
        return [Paper(*row) for row in rows], total_num


    @staticmethod
    def get_citing_papers_by_pid(pid):
        rows = app.db.execute(
            '''
            SELECT papers.pid, title, year, conference
            FROM papers
            WHERE pid IN (SELECT cite_pid
                FROM citation
                WHERE pid = :pid)
            ORDER BY pid
            ''',pid=pid)
        return [Paper(*row) for row in rows]
    
class Statistic:
    def __init__(self, category, count):
        self.category = category
        self.count = count 

    @staticmethod 
    def get_year_statistic():
        rows = app.db.execute(
        '''
        SELECT year, count(*) as cnt
        FROM papers
        GROUP BY year
        ORDER BY cnt DESC
        LIMIT 5
        ''')
        return [Statistic(*row) for row in rows]

    @staticmethod 
    def get_author_statistic():
        rows = app.db.execute(
        '''
        SELECT a.author , count(*) as cnt
        FROM papers as p, authorship as a 
        WHERE p.pid = a.pid and a.author!='Staff'
        GROUP BY a. author
        ORDER BY cnt DESC
        LIMIT 5 
        ''')
        return [Statistic(*row) for row in rows]


class Authors:
    def __init__(self, pid, author):
        self.pid = pid
        self.author = author

    @staticmethod
    def get_by_pid(pid):
        rows = app.db.execute(
            '''
            SELECT pid, author
            FROM authorship
            WHERE pid = :pid
            ''', pid=pid)
        return [Authors(*row) for row in rows]
    
    def get_pid_by_author(author):
        rows = app.db.execute(
            '''
            SELECT pid, author
            FROM authorship
            WHERE author =:author
            ''', author=author
        )
        return [Authors(*row) for row in rows]

class Abstract:
    def __init__(self, pid, abstract):
        self.pid = pid
        self.abstract = abstract

    @staticmethod
    def get_by_pid(pid):
        rows = app.db.execute(
            '''
            SELECT pid, abstract
            FROM abstract
            WHERE pid = :pid
            ''', pid=pid)
        if len(rows) == 0:
            return None
        return Abstract(*(rows[0]))