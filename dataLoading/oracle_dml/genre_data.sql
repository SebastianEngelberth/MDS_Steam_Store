BEGIN
 INSERT INTO genre (genre_id, name) VALUES (1, 'Accounting');
 INSERT INTO genre (genre_id, name) VALUES (2, 'Action');
 INSERT INTO genre (genre_id, name) VALUES (3, 'Adventure');
 INSERT INTO genre (genre_id, name) VALUES (4, 'Animation & Modeling');
 INSERT INTO genre (genre_id, name) VALUES (5, 'Audio Production');
 INSERT INTO genre (genre_id, name) VALUES (6, 'Casual');
 INSERT INTO genre (genre_id, name) VALUES (7, 'Design & Illustration');
 INSERT INTO genre (genre_id, name) VALUES (8, 'Documentary');
 INSERT INTO genre (genre_id, name) VALUES (9, 'Early Access');
 INSERT INTO genre (genre_id, name) VALUES (10, 'Education');
 INSERT INTO genre (genre_id, name) VALUES (11, 'Free to Play');
 INSERT INTO genre (genre_id, name) VALUES (12, 'Game Development');
 INSERT INTO genre (genre_id, name) VALUES (13, 'Gore');
 INSERT INTO genre (genre_id, name) VALUES (14, 'Indie');
 INSERT INTO genre (genre_id, name) VALUES (15, 'Massively Multiplayer');
 INSERT INTO genre (genre_id, name) VALUES (16, 'Nudity');
 INSERT INTO genre (genre_id, name) VALUES (17, 'Photo Editing');
 INSERT INTO genre (genre_id, name) VALUES (18, 'RPG');
 INSERT INTO genre (genre_id, name) VALUES (19, 'Racing');
 INSERT INTO genre (genre_id, name) VALUES (20, 'Sexual Content');
 INSERT INTO genre (genre_id, name) VALUES (21, 'Simulation');
 INSERT INTO genre (genre_id, name) VALUES (22, 'Software Training');
 INSERT INTO genre (genre_id, name) VALUES (23, 'Sports');
 INSERT INTO genre (genre_id, name) VALUES (24, 'Strategy');
 INSERT INTO genre (genre_id, name) VALUES (25, 'Tutorial');
 INSERT INTO genre (genre_id, name) VALUES (26, 'Utilities');
 INSERT INTO genre (genre_id, name) VALUES (27, 'Video Production');
 INSERT INTO genre (genre_id, name) VALUES (28, 'Violent');
 INSERT INTO genre (genre_id, name) VALUES (29, 'Web Publishing');
END;

SELECT COUNT(*)
       FROM v$transaction t, v$session s, v$mystat m
      WHERE t.ses_addr = s.saddr
        AND s.sid = m.sid
        AND ROWNUM = 1;
