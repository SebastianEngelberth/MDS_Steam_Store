
LOAD CSV WITH HEADERS FROM 'file:///CATEGORY.csv' AS row
MERGE (category:Category {category_id: row.CATEGORY_ID})
  ON CREATE SET category.name = row.NAME;


LOAD CSV WITH HEADERS FROM 'file:///GENRE.csv' AS row
MERGE (genre:Genre {genre_id: row.GENRE_ID})
  ON CREATE SET genre.name = row.NAME;


LOAD CSV WITH HEADERS FROM 'file:///USER.csv' AS row
MERGE (user:User {user_id: row.USER_ID})
  ON CREATE SET user.username = row.USERNAME, user.email = row.EMAIL, user.age = row.AGE, user.password = row.PASSWORD;


LOAD CSV WITH HEADERS FROM 'file:///VIDEOGAME.csv' AS row
MERGE (videogame:Videogame {videogame_id: row.VIDEOGAME_ID})
  ON CREATE SET videogame.name = row.NAME, videogame.release_date = row.RELEASE_DATE, videogame.required_age = toInteger(row.REQUIRED_AGE), videogame.price = toFloat(row.PRICE), videogame.positive_ratings = toInteger(row.POSITIVE_RATINGS), videogame.negative_ratings = toInteger(row.NEGATIVE_RATINGS);


LOAD CSV WITH HEADERS FROM 'file:///DEVELOPER.csv' AS row
MERGE (developer:Developer {developer_id: row.DEVELOPER_ID})
  ON CREATE SET developer.name = row.NAME;


LOAD CSV WITH HEADERS FROM 'file:///PUBLISHER.csv' AS row
MERGE (publisher:Publisher {publisher_id: row.PUBLISHER_ID})
  ON CREATE SET publisher.name = row.NAME;


LOAD CSV WITH HEADERS FROM 'file:///TAG.csv' AS row
MERGE (tag:Tag {tag_id: row.TAG_ID})
  ON CREATE SET tag.name = row.NAME;


CREATE INDEX categoryid FOR (c:Category) ON (c.category_id);
CREATE INDEX videogame_name FOR (v:Videogame) ON (v.name);
CREATE INDEX videogameid FOR (v:Videogame) ON (v.videogame_id);
CREATE INDEX genreid FOR (g:Genre) ON (g.genre_id);
CREATE INDEX userid FOR (u:User) ON (u.user_id);
CREATE INDEX developerid FOR (d:Developer) ON (d.developer_id);
CREATE INDEX publisherid FOR (p:Publisher) ON (p.publisher_id);
CREATE INDEX tagid FOR (t:Tag) ON (t.tag_id);
CALL db.awaitIndexes();


LOAD CSV WITH HEADERS FROM 'file:///BELONGS_TO_CAT.csv' AS row
MATCH (category:Category {category_id: row.CATEGORY_ID})
MATCH (videogame:Videogame {videogame_id: row.VIDEOGAME_ID})
MERGE (videogame)-[:BELONGS_TO_CAT]->(category);


LOAD CSV WITH HEADERS FROM 'file:///BELONGS_TO_GEN.csv' AS row
MATCH (genre:Genre {genre_id: row.GENRE_ID})
MATCH (videogame:Videogame {videogame_id: row.VIDEOGAME_ID})
MERGE (videogame)-[:BELONGS_TO_GEN]->(genre);


LOAD CSV WITH HEADERS FROM 'file:///DEVELOPS.csv' AS row
MATCH (developer:Developer {developer_id: row.DEVELOPER_ID})
MATCH (videogame:Videogame {videogame_id: row.VIDEOGAME_ID})
MERGE (developer)-[:DEVELOPS]->(videogame);


LOAD CSV WITH HEADERS FROM 'file:///FRIENDS_WITH.csv' AS row
MATCH (user1:User {user_id: row.USER1_ID})
MATCH (user2:User {user_id: row.USER2_ID})
MERGE (user1)-[:FRIENDS_WITH]->(user2);


LOAD CSV WITH HEADERS FROM 'file:///FRIENDS_WITH.csv' AS row
MATCH (user1:User {user_id: row.USER1_ID})
MATCH (user2:User {user_id: row.USER2_ID})
MERGE (user2)-[:FRIENDS_WITH]->(user1);


LOAD CSV WITH HEADERS FROM 'file:///OWNS.csv' AS row
MATCH (user:User {user_id: row.USER_ID})
MATCH (videogame:Videogame {videogame_id: row.VIDEOGAME_ID})
MERGE (user)-[o:OWNS]->(videogame)
  ON CREATE SET o.purchase_date = row.PURCHASE_DATE, o.playtime = toInteger(row.PLAYTIME);


LOAD CSV WITH HEADERS FROM 'file:///PUBLISHES.csv' AS row
MATCH (publisher:Publisher {publisher_id: row.PUBLISHER_ID})
MATCH (videogame:Videogame {videogame_id: row.VIDEOGAME_ID})
MERGE (publisher)-[:PUBLISHES]->(videogame);


LOAD CSV WITH HEADERS FROM 'file:///TAGGED_WITH.csv' AS row
MATCH (tag:Tag {tag_id: row.TAG_ID})
MATCH (videogame:Videogame {videogame_id: row.VIDEOGAME_ID})
MERGE (videogame)-[:TAGGED_WITH]->(tag);
