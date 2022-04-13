\COPY Auth FROM 'Auth.csv' WITH DELIMITER ',' NULL '' CSV
-- since id is auto-generated; we need the next command to adjust the counter
-- for auto-generation so next INSERT will not clash with ids loaded above:
SELECT pg_catalog.setval('public.auth_uid_seq',
                         (SELECT MAX(uid)+1 FROM Auth),
                         false);

\COPY Users FROM 'Users.csv' WITH DELIMITER ',' NULL '' CSV
-- since id is auto-generated; we need the next command to adjust the counter
-- for auto-generation so next INSERT will not clash with ids loaded above:
SELECT pg_catalog.setval('public.users_uid_seq',
                         (SELECT MAX(uid)+1 FROM Users),
                         false);

\COPY User_browse FROM 'User_browse.csv' WITH DELIMITER ',' NULL '' CSV

\COPY User_cart FROM 'User_cart.csv' WITH DELIMITER ',' NULL '' CSV

\COPY Users_cite_history FROM 'User_cite_history.csv' WITH DELIMITER ',' NULL '' CSV

\COPY Collections FROM 'Collections.csv' WITH DELIMITER ',' NULL '' CSV

-- paper research platform table load
\COPY Papers FROM 'papers.csv' WITH DELIMITER ',' NULL '' CSV


\COPY Citation FROM 'citation.csv' WITH DELIMITER ',' NULL '' CSV

\COPY Authorship FROM 'authorship.csv' WITH DELIMITER ',' NULL '' CSV

\COPY Abstract FROM 'abstract.csv' WITH DELIMITER ',' NULL '' CSV

\COPY Comment FROM 'comment.csv' WITH DELIMITER ',' NULL '' CSV
