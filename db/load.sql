\COPY Auth FROM 'Auth.csv' WITH DELIMITER ',' NULL '' CSV
-- since id is auto-generated; we need the next command to adjust the counter
-- for auto-generation so next INSERT will not clash with ids loaded above:
SELECT pg_catalog.setval('public.auth_id_seq',
                         (SELECT MAX(id)+1 FROM Auth),
                         false);

-- initial mini amazon table load
\COPY Users FROM 'Users.csv' WITH DELIMITER ',' NULL '' CSV
-- since id is auto-generated; we need the next command to adjust the counter
-- for auto-generation so next INSERT will not clash with ids loaded above:
SELECT pg_catalog.setval('public.users_id_seq',
                         (SELECT MAX(id)+1 FROM Users),
                         false);

-- paper research platform table load
\COPY papers FROM 'papers.csv' WITH DELIMITER ',' NULL '' CSV


\COPY citation FROM 'citation.csv' WITH DELIMITER ',' NULL '' CSV

\COPY authorship FROM 'authorship.csv' WITH DELIMITER ',' NULL '' CSV

\COPY abstract FROM 'abstract.csv' WITH DELIMITER ',' NULL '' CSV

