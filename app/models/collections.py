from flask import current_app as app
from .paper import Paper

class Collections:
    def __init__(self, uid, collection_name, pid):
        self.uid = uid
        self.collection_name=collection_name
        self.pid = pid

    @staticmethod
    def get_pids(uid,collection_name):
        rows = app.db.execute('''
SELECT pid
FROM Collections
WHERE uid = :uid and collection_name =:collection_name
''',
                              uid=uid,collection_name=collection_name)
        pids=[]
        if rows is None:
            return None
        for row in rows:
        # if create an empty collection, we insert a row that pid==-1, so we need to filter that pid
            if row[0]!=-1:
                pids.append(row[0])
        # return a list of pids in that collection
        return pids
    
    @staticmethod
    def get_papers(uid,collection_name):
        rows = app.db.execute('''
SELECT Papers.pid,title,year,conference
FROM Collections, Papers
WHERE uid = :uid and collection_name =:collection_name and Collections.pid = Papers.pid
''',
                              uid=uid,collection_name=collection_name)
        if rows is None:
            return None
        return [Paper(*row) for row in rows]

    @staticmethod
    def check_paper_in_collection(uid,collection_name,pid):
        rows = app.db.execute('''
SELECT *
FROM Collections
WHERE uid = :uid and collection_name =:collection_name and pid =:pid
''',
                              uid=uid,collection_name=collection_name,pid=pid)
        return True if rows is not None else False
    
    @staticmethod
    def add_paper_in_collection(uid,collection_name,pid):
        rows = app.db.execute('''
INSERT INTO Collections(uid, collection_name, pid)
VALUES(:uid, :collection_name, :pid)
RETURNING pid
''',
                              uid=uid,collection_name=collection_name,pid=pid)
        return rows[0][0] if rows is not None else None

    @staticmethod
    def remove_paper_from_collection(uid,collection_name,pid):
        rows = app.db.execute('''
delete from Collections
where uid= :uid and collection_name =:collection_name and pid = :pid
returning pid
''',
                              uid=uid,collection_name=collection_name,pid=pid)
        return Collections(*(rows[0])) if rows is not None else None
    
    @staticmethod
    def check_same_collection_name(collection_name):
        rows = app.db.execute('''
SELECT count(*)
FROM Collections
WHERE collection_name =:collection_name
''',
                            collection_name=collection_name)
        print("same name:",rows)
        return True if rows is not None and rows[0][0]>0 else False
    
    # if create an empty collection, we insert a row that pid==-1
    @staticmethod
    def add_new_collection(uid,collection_name):
        rows = app.db.execute('''
INSERT INTO Collections(uid, collection_name, pid)
VALUES(:uid, :collection_name, -1)
        ''',
        uid=uid,collection_name=collection_name)
        print("rows:",rows)
        print(collection_name)
        # a number of inserted tuples
        return rows if rows is not None else None
    
    @staticmethod
    def rename_collection(uid,old_name,new_name):
        rows = app.db.execute('''
update Collections
set collection_name =:new_name
WHERE uid =:uid and collection_name =:old_name
        ''',
        uid=uid, old_name=old_name, new_name=new_name)
        return rows if rows is not None else None

    @staticmethod
    def delete_collection(uid,collection_name):
        rows = app.db.execute('''
delete from Collections
where uid= :uid and collection_name =:collection_name
''',
                            uid=uid, collection_name=collection_name)
        return Collections(*(rows[0])) if rows is not None else None
    
    # get name and number of papers of each collection
    # first create collection, then add papers in them
    @staticmethod
    def get_each_collection(uid):
        rows = app.db.execute('''
select collection_name, count(*)-1
from Collections
where uid= :uid 
group by collection_name
''',
                            uid=uid)
        return  rows if rows is not None else None
