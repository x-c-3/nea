-- init.sql

-- Create the table of users
CREATE TABLE IF NOT EXISTS User (
	username VARCHAR(30) PRIMARY KEY NOT NULL, -- username, max 30 letters so you cant eat up all the memory, uniquely identifies each user
	password VARCHAR(64) NOT NULL, -- password hashed with SHA256, hence 64 chars. I will be using SHA256 to hash passwords since it has a very small collision rate.
	lastLogin TEXT NOT NULL,
	lastStreakLogin TEXT NOT NULL,
	streak INTEGER NOT NULL
);

-- store data about all the challenges
CREATE TABLE IF NOT EXISTS Challenge (
	challengeName VARCHAR(50) PRIMARY KEY NOT NULL, -- stores the name of the challenge, max 50 chars
	description VARCHAR(500) NOT NULL, -- stores the challenge description, max 500 chars
	shortDesc VARCHAR(500) NOT NULL, -- challenge description that is shown on the challenges page
	difficulty INTEGER NOT NULL, -- stores the challenge difficulty
	points INTEGER NOT NULL, -- stores the challenge points
	category VARCHAR(20) NOT NULL, -- stores the category, max 20 chars, category names should not be very long
	flag TEXT NOT NULL, -- the flag for solving the challenge
	source BOOL NOT NULL, -- if the challenge has source code provided to players
	courseName VARCHAR(50) NOT NULL, -- the name of the course this challenge is associated with
	levelNo INTEGER NOT NULL, -- the level number in that course that this challenge is on
	FOREIGN KEY (courseName, levelNo) REFERENCES Level(courseName, levelNo)
);

-- relates challenges and users who have solved the challenges
CREATE TABLE IF NOT EXISTS ChallengeSolve (
	challengeName VARCHAR(50), -- challengeName will link each record to a challenge
	username VARCHAR(30), -- username will link each record to a user
	firstBlood BOOL NOT NULL, -- if the solve was a first blood
	FOREIGN KEY (challengeName) REFERENCES Challenge(name), -- link the Assignment and Challenge tables
	FOREIGN KEY (username) REFERENCES User(username), -- link the Assignment and Classroom tables
	PRIMARY KEY (challengeName, username) -- composite primary key
);

CREATE TABLE IF NOT EXISTS Level (
	courseName VARCHAR(50) NOT NULL,
	levelNo INTEGER NOT NULL,
	infos TEXT NOT NULL, -- JSON array of strings, each individual pages
	FOREIGN KEY (courseName) REFERENCES Course(courseName),
	PRIMARY KEY (levelNo, courseName)
);

-- store data about all the courses
CREATE TABLE IF NOT EXISTS Course (
	courseName VARCHAR(50) PRIMARY KEY NOT NULL, -- stores the name of the course, max 50 chars, uniquely
	shortDesc VARCHAR(500) NOT NULL -- course description shown on the courses page
);

-- store data about solves on all the courses
CREATE TABLE IF NOT EXISTS CourseSolve (
	courseName VARCHAR(50), -- courseName links each solve to a course
	username VARCHAR(30), -- username will link each solve to a user
	FOREIGN KEY (courseName) REFERENCES Course(name), -- link the Course and CourseSolve tables
	FOREIGN KEY (username) REFERENCES User(username), -- link the User and CourseSolve tables
	PRIMARY KEY (courseName, username) -- composite primary key
);