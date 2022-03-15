-- data for user authentication (registration & login)
CREATE TABLE AUTH (
    id INT NOT NULL PRIMARY KEY GENERATED BY DEFAULT AS IDENTITY,
    email VARCHAR UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    firstname VARCHAR(255) NOT NULL,
    lastname VARCHAR(255) NOT NULL,
    school VARCHAR(255) NOT NULL
);
 
-- data for user profile & dashboard
CREATE TABLE USER (
	id INT NOT NULL PRIMARY KEY  GENERATED BY DEFAULT AS IDENTITY,
	nickname VARCHAR(255) UNIQUE NOT NULL, 
	citeNum INTEGER DEFAULT 0, 
	research_interest VARCHAR(255)
)
 
-- user citation cart
CREATE TABLE User_Cart (
	uid INT NOT NULL,
cite_pid INT NOT NULL
time_added timestamp without time zone NOT NULL DEFAULT (current_timestamp AT TIME ZONE 'UTC')
)
 
-- user browser history of papers
CREATE TABLE User_browse (
	uid INT NOT NULL,
	browsed_pid INT NOT NULL
time_browsed timestamp without time zone NOT NULL DEFAULT (current_timestamp AT TIME ZONE 'UTC')
)
 
-- paper database
CREATE TABLE Papers (
    pid INT NOT NULL PRIMARY KEY GENERATED BY DEFAULT AS IDENTITY,
	title TEXT NOT NULL,
	year INTEGER, 
	conference TEXT
)
 
 
--paper authors
CREATE TABLE Authorship (
pid INT NOT NULL,
name VARCHAR(255) NOT NULL,
)
 
-- citation relationship among papers
CREATE TABLE citation (
	pid INT NOT NULL,
cite_pid INT NOT NULL
)
 
-- user’s collection
CREATE TABLE Collections(
	uid INT NOT NULL,	
	collection_name VARCHAR(255) UNIQUE NOT NULL,
	pid INT NOT NULL
)