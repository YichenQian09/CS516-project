from flask import current_app as app

# CREATE TABLE Comment (
#     pid INT NOT NULL,
#     uid INT NOT NULL, 
#     star INT NOT NULL,
#     comment_sum TEXT,
#     comment_text TEXT,
#     time_submitted timestamp without time zone NOT NULL DEFAULT (now()::timestamp(0)),
#     helpful_vote INT NOT NULL, 
#     PRIMARY KEY (pid,uid)
# );

class Comment:
    def __init__(self,pid,uid,star,comment_sum,comment_text,time_submitted,helpful_vote):
        self.pid = pid
        self.uid = uid
        self.star = star
        self.comment_sum = comment_sum
        self.comment_text = comment_text
        self.time_submitted = time_submitted 
        self.helpful_vote = helpful_vote

    @staticmethod
    def add_comment(pid,uid,star,comment_sum,comment_text,helpful_vote):
        rows = app.db.execute('''
            INSERT INTO Comment(pid,uid,star,comment_sum, comment_text,time_submitted,helpful_vote)
            VALUES(:pid,:uid,:star,:comment_sum,:comment_text, now()::timestamp(0),:helpful_vote)
            ''', pid=pid,uid=uid,star=star,comment_sum=comment_sum,comment_text=comment_text,
                helpful_vote=helpful_vote)
        print("add_comment: ",rows)
        #return the pid of the added 
        return rows==1

    @staticmethod
    def fetch_comment_by_pid(pid):
        rows = app.db.execute(
            '''
            SELECT *
            FROM Comment
            WHERE pid = :pid
            ORDER BY helpful_vote DESC, time_submitted DESC
            '''
        ,pid= pid)
        return [Comment(*row) for row in rows]

    @staticmethod
    def fetch_comment_by_uid(uid):
        rows = app.db.execute(
            '''
            SELECT *
            FROM Comment
            WHERE uid = :uid
            ORDER BY helpful_vote DESC, time_submitted DESC
            '''
        ,uid= uid)
        return [Comment(*row) for row in rows]

    @staticmethod
    def fetch_comment_by_pid_uid(uid,pid):
        rows = app.db.execute(
            '''
            SELECT *
            FROM Comment
            WHERE uid = :uid AND pid = :pid
            '''
        ,uid= uid,pid=pid)
        return Comment(*rows[0]) 

    @staticmethod
    def delete_comment_by_pid_uid(pid,uid):
        rows = app.db.execute(
            '''
            DELETE FROM Comment
            WHERE pid = :pid AND uid = :uid;
            '''
        ,pid= pid,uid=uid)
        print("delete_comment:", rows)
        assert rows==1

    @staticmethod
    def check_if_commented_by_pid_uid(pid,uid):
        rows = app.db.execute(
            '''
            SELECT *
            FROM Comment
            WHERE pid = :pid AND uid = :uid
            '''
        ,pid= pid,uid=uid)
        print("check:", rows)
        return len(rows)>0

    @staticmethod
    def edit_comment_by_pid_uid(pid,uid,star,updated_sum, updated_comment):
        rows = app.db.execute(
            '''
            UPDATE Comment
            SET comment_text = :updated_comment,
                comment_sum = :updated_sum,
                star = :star,
                time_submitted = now()::timestamp(0)
            WHERE pid = :pid AND uid=:uid
            '''
        ,pid= pid,uid=uid,star=star,updated_sum = updated_sum,
        updated_comment = updated_comment)
        assert rows ==1

    @staticmethod
    def get_average_star(pid):
        rows = app.db.execute(
            '''
            SELECT star
            FROM Comment
            WHERE pid = :pid 
            '''
        ,pid= pid)
        row_unwind = [item for sublist in rows for item in sublist]
        print(row_unwind)
        return sum(row_unwind), len(row_unwind)

    @staticmethod
    def upvote_comment(pid,uid):
        rows = app.db.execute(
            '''
            UPDATE Comment
            SET helpful_vote= helpful_vote+1
            WHERE pid = :pid AND uid=:uid
            '''
        ,pid= pid,uid=uid)
        print(rows)
        assert rows== 1
      
    
    @staticmethod
    def cancel_upvote(pid,uid):
        rows = app.db.execute(
            '''
            UPDATE Comment
            SET helpful_vote= helpful_vote-1
            WHERE pid = :pid AND uid=:uid
            '''
        ,pid= pid,uid=uid)
        print(rows)
        assert rows == 1

    @staticmethod
    def recommend_by_keyword(k1,k2,k3):
        sql_str = '''WITH temp as (SELECT p.pid FROM Papers as p WHERE 
           (p.title LIKE '%'''+k1+"%') OR (p.title LIKE '%"+k1+"%') OR (p.title LIKE '%"+k3+'''%'))
           SELECT c.pid
           FROM Comment as c, temp
           WHERE c.pid = temp.pid 
           GROUP BY c.pid
           ORDER BY avg(c.star) DESC 
           LIMIT 5
           '''
        rows = app.db.execute(sql_str)
        rows = [r[0] for r in rows]
        print(rows)
        return rows


class Helpful:
    def __init__(self,pid,uid,upvote_by_uid):
        self.pid = pid
        self.uid = uid
        self.upvote_by_uid = upvote_by_uid

    @staticmethod
    def upvote_comment(pid,uid,upvote_by_uid):
        rows = app.db.execute('''
            INSERT INTO Helpful(pid,uid,upvote_by_uid)
            VALUES(:pid,:uid,:upvote_by_uid)
            ''', pid=pid,uid=uid,upvote_by_uid=upvote_by_uid)
        print("add_comment: ",rows)
        assert rows==1

    @staticmethod
    def check_if_upvoted(pid,uid,upvote_by_uid):
        rows = app.db.execute(
            '''
            SELECT *
            FROM Helpful
            WHERE pid = :pid AND uid = :uid AND upvote_by_uid = :upvote_by_uid;
            '''
        ,pid= pid,uid=uid,upvote_by_uid=upvote_by_uid)
        print("check:", rows)
        return len(rows)>0

    def cancel_upvote(pid,uid,upvote_by_uid):
        rows = app.db.execute(
            '''
            DELETE FROM Helpful
            WHERE pid = :pid AND uid = :uid AND upvote_by_uid = :upvote_by_uid;
            '''
        ,pid= pid,uid=uid,upvote_by_uid=upvote_by_uid)
        print("delete_comment:", rows)
        assert rows==1

        