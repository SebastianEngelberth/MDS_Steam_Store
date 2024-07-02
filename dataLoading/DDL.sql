

CREATE TABLE "USER"(
    user_id NUMBER PRIMARY KEY,
    username VARCHAR2(50) NOT NULL,
    email VARCHAR2(50) NOT NULL,
    age NUMBER NOT NULL,
    password VARCHAR2(50) NOT NULL
);

CREATE TABLE Developer(
    developer_id NUMBER PRIMARY KEY,
    name VARCHAR2(255) NOT NULL
);


CREATE TABLE Videogame (
    videogame_id NUMBER PRIMARY KEY,
    name VARCHAR2(255) NOT NULL,
    release_date DATE NOT NULL,
    required_age NUMBER NOT NULL,
    price NUMBER NOT NULL,
    positive_ratings NUMBER NOT NULL,
    negative_ratings NUMBER NOT NULL
);

CREATE TABLE Publisher (
    publisher_id NUMBER PRIMARY KEY,
    name VARCHAR2(255) NOT NULL
);

CREATE TABLE Genre (
    genre_id NUMBER PRIMARY KEY,
    name VARCHAR2(255) NOT NULL
);

CREATE TABLE Category (
    category_id NUMBER PRIMARY KEY,
    name VARCHAR2(255) NOT NULL
);

CREATE TABLE Tag (
    tag_id NUMBER PRIMARY KEY,
    name VARCHAR2(255) NOT NULL
);

CREATE TABLE Friends_with (
    user1_id NUMBER NOT NULL,
    user2_id NUMBER NOT NULL,
    CONSTRAINT pk_friends_with PRIMARY KEY (user1_id, user2_id)
);

CREATE TABLE Owns (
    user_id NUMBER NOT NULL,
    videogame_id NUMBER NOT NULL,
    purchase_date DATE NOT NULL,
    playtime NUMBER NOT NULL,
    CONSTRAINT pk_owns PRIMARY KEY (user_id, videogame_id)
);

CREATE TABLE Belongs_to_gen (
    genre_id NUMBER NOT NULL,
    videogame_id NUMBER NOT NULL,
    CONSTRAINT pk_videogame_gen PRIMARY KEY (genre_id, videogame_id)
);

CREATE TABLE Belongs_to_cat (
    category_id NUMBER NOT NULL,
    videogame_id NUMBER NOT NULL,
    CONSTRAINT pk_videogame_cat PRIMARY KEY (category_id, videogame_id)
);

CREATE TABLE Tagged_with (
    tag_id NUMBER NOT NULL,
    videogame_id NUMBER NOT NULL,
    amount NUMBER NOT NULL,
    CONSTRAINT pk_tagged_with PRIMARY KEY (tag_id, videogame_id)
);

CREATE TABLE Publishes (
    publisher_id NUMBER NOT NULL,
    videogame_id NUMBER NOT NULL,
    CONSTRAINT pk_publishes PRIMARY KEY (publisher_id, videogame_id)
);

CREATE TABLE Develops (
    developer_id NUMBER NOT NULL,
    videogame_id NUMBER NOT NULL,
    CONSTRAINT pk_develops PRIMARY KEY (developer_id, videogame_id)
);


ALTER TABLE Friends_with ADD CONSTRAINT fk_friends_with_user1 FOREIGN KEY (user1_id) REFERENCES "USER"(user_id);
ALTER TABLE Friends_with ADD CONSTRAINT fk_friends_with_user2 FOREIGN KEY (user2_id) REFERENCES "USER"(user_id);

ALTER TABLE Owns ADD CONSTRAINT fk_owns_user FOREIGN KEY (user_id) REFERENCES "USER"(user_id);
ALTER TABLE Owns ADD CONSTRAINT fk_owns_videogame FOREIGN KEY (videogame_id) REFERENCES Videogame(videogame_id);

ALTER TABLE Belongs_to_gen ADD CONSTRAINT fk_belongs_genre FOREIGN KEY (genre_id) REFERENCES Genre(genre_id);
ALTER TABLE Belongs_to_gen ADD CONSTRAINT fk_belongs_videogame FOREIGN KEY (videogame_id) REFERENCES Videogame(videogame_id);

ALTER TABLE Belongs_to_cat ADD CONSTRAINT fk_belongs_category FOREIGN KEY (category_id) REFERENCES Category(category_id);
ALTER TABLE Belongs_to_cat ADD CONSTRAINT fk_belongs_cat_videogame FOREIGN KEY (videogame_id) REFERENCES Videogame(videogame_id);

ALTER TABLE Tagged_with ADD CONSTRAINT fk_tagged_tag FOREIGN KEY (tag_id) REFERENCES Tag(tag_id);
ALTER TABLE Tagged_with ADD CONSTRAINT fk_tagged_videogame FOREIGN KEY (videogame_id) REFERENCES Videogame(videogame_id);

ALTER TABLE Publishes ADD CONSTRAINT fk_publishes_publisher FOREIGN KEY (publisher_id) REFERENCES Publisher(publisher_id);
ALTER TABLE Publishes ADD CONSTRAINT fk_publishes_videogame FOREIGN KEY (videogame_id) REFERENCES Videogame(videogame_id);

ALTER TABLE Develops ADD CONSTRAINT fk_develops_developer FOREIGN KEY (developer_id) REFERENCES Developer(developer_id);
ALTER TABLE Develops ADD CONSTRAINT fk_develops_videogame FOREIGN KEY (videogame_id) REFERENCES Videogame(videogame_id);
