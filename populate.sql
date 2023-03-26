INSERT INTO User VALUES ("administrator", "4194d1706ed1f408d5e02d672777019f4d5385c766a8c6ca8acba3167d36a7b9", "01/01/1970 00:00:00", "01/01/1970 00:00:00", 1);

INSERT INTO User VALUES ("user", "04f8996da763b7a969b1028ee3007569eaf3a635486ddab211d512c85b9df8fb", "01/01/1970 00:00:00", "01/01/1970 00:00:00", 1);

-- Add the four courses
INSERT INTO Course VALUES ("JavaScript", "Learn the basics of the client-side and explore the ubiquitous scripting language of the Web.");
INSERT INTO Course VALUES ("SQL", "Learn about the fundamentals of what Structured Query Language (SQL) is, its applications, and the dangers of SQL injection.");
INSERT INTO Course VALUES ("Cookies", "How does a website remember who you are? Chances are that it's via cookies. Learn about what cookies are and common misconceptions around cookies. It is recommended that you complete the JavaScript course before attempting this course.");
INSERT INTO Course VALUES ("SSRF", "Test your skills with this more difficult course covering Server Side Request Forgery (SSRF).");

-- Add the information snippets

-- JavaScript

-- Level 1

INSERT INTO Level VALUES ("JavaScript", 1, "");

-- Add challenges

INSERT INTO Challenge VALUES ("challenge-1", "Description", "Short Description", "medium", 300, "SQL", "flag{flag}", false, "course-1", 1);

-- INSERT INTO ChallengeSolve VALUES ("challenge-1", "administrator", true);