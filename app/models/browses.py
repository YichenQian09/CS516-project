from flask import current_app as app
from .paper import Paper
import time

class Browses:
    def __init__(self, uid, browsed_pid, time_browsed):
        self.uid = uid
        self.browsed_pid=browsed_pid
        self.time_browsed = time_browsed
        
    @staticmethod
    def get_papers(uid,timerange):
        if timerange == 'all':
            rows = app.db.execute('''
    SELECT Papers.pid,title,year,conference
    FROM User_browse, Papers
    WHERE uid = :uid and User_browse.browsed_pid = Papers.pid
    order by time_browsed desc
    ''',
                              uid=uid)
        elif timerange == 'today':
            rows = app.db.execute('''
    SELECT Papers.pid,title,year,conference
    FROM User_browse, Papers
    WHERE uid = :uid and User_browse.browsed_pid = Papers.pid
    and time_browsed >= current_date + time '00:00'
    and time_browsed <= current_date + time '23:59:59'
    order by time_browsed desc
    ''',
                                uid=uid)
        elif timerange == 'last_week':
            rows = app.db.execute('''
    SELECT Papers.pid,title,year,conference
    FROM User_browse, Papers
    WHERE uid = :uid and User_browse.browsed_pid = Papers.pid
    and time_browsed >= current_date - 7 + time '00:00'
    and time_browsed <= current_date + time '23:59:59'
    order by time_browsed desc
    ''',
                                uid=uid)
        if rows is None:
            return None
        return [Paper(*row) for row in rows]

    @staticmethod
    def record_browse(uid,pid):
        records= app.db.execute('''
    SELECT browsed_pid
    FROM User_browse
    WHERE uid = :uid and browsed_pid = :pid
    ''',
                                uid=uid,pid=pid)
        if records is None:
            return None
        # is it the true statement?
        print("is record?:",len(records)>0)
        if len(records)>0:
            rows=app.db.execute('''
    update User_browse
    set time_browsed = now()::timestamp(0)
    WHERE uid = :uid and browsed_pid = :pid
    ''',
                                uid=uid,pid=pid)
        else:
             rows=app.db.execute('''
    insert into User_browse(uid,browsed_pid,time_browsed)
    values(:uid,:pid,now()::timestamp(0))
    ''',
                                uid=uid,pid=pid)
        if rows is None:
            return None
        return rows