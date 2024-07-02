// Get most played games by ownership
MATCH (v:Videogame)<-[:OWNS]-()
RETURN v.name AS Name, count(v) AS Count
ORDER BY Count DESC


// Get game by genre, tag, category, publisher and developer
MATCH (v:Videogame)-[:BELONGS_TO_GEN]->(g:Genre),
      (v)-[:BELONGS_TO_CAT]->(c:Category),
      (d:Developer)-[:DEVELOPS]->(v),
      (p:Publisher)-[:PUBLISHES]->(v),
      (v)-[:TAGGED_WITH]->(t:Tag)
WHERE g.name = 'Action'
  AND c.name = 'Online Multi-Player'
  AND p.name = 'Valve'
  AND d.name = 'Valve'
  AND t.name = 'Multiplayer'
RETURN v.name


// Get friends of friends of a user
MATCH (u1:User {user_id: "23478"})-[:FRIENDS_WITH*2]-(u3)
WHERE NOT (u1)-[:FRIENDS_WITH]-(u3) AND u1 <> u3
RETURN DISTINCT u3.username


// Get all friends of friends of friends of a user (Not in Paper)
MATCH (u1:User {user_id: "23478"})-[:FRIENDS_WITH*3]-(u3)
WHERE NOT (u1)-[:FRIENDS_WITH]-(u3) AND u1 <> u3
RETURN DISTINCT u3.username


// Get friend recommendation based on how many of the ten most played games of a user they own
MATCH (User {user_id: "23478"})-[o1:OWNS]->(v1:Videogame)
WITH o1, v1
ORDER BY o1.playtime DESC
LIMIT 10

MATCH (u2:User)-[:OWNS]->(v2:Videogame)
WHERE v2.videogame_id IN [v1.videogame_id] AND u2.user_id <> "23478"
WITH u2, COUNT(*) AS GamesOwned
WHERE GamesOwned >= 2
RETURN u2.username, u2.user_id, GamesOwned


// Get game recommendation based on players who played a chosen game
MATCH (v:Videogame {name: 'Snakebird'})<-[:OWNS]-(u:User)-[:OWNS]->(v1:Videogame)
WHERE v.videogame_id <> v1.videogame_id
RETURN v1.name, COUNT(v1.videogame_id) AS GamesCount
ORDER BY GamesCount DESC


// Get game recommendation based on the three most played games of a user (2 Tags match, min -30% Ownership)
MATCH (u:User {user_id: "23059"})-[o:OWNS]->(v1:Videogame)
WITH v1
ORDER BY o.playtime DESC
LIMIT 1

MATCH (v1)-[:TAGGED_WITH]->(t:Tag)<-[:TAGGED_WITH]-(v2:Videogame)
WHERE NOT v1 = v2

WITH v1, v2, count(DISTINCT t) AS CommonTags
WHERE CommonTags >= 2

WITH v1, v2, CommonTags
MATCH (u1)-[:OWNS]->(v1)
MATCH (u2)-[:OWNS]->(v2)
WITH v1, v2, CommonTags, COUNT(DISTINCT u1) AS Owner1, COUNT(DISTINCT u2) AS Owner2
WHERE Owner2 >= Owner1 * 0.7

WITH v2, CommonTags
RETURN v2.videogame_id, CommonTags
ORDER BY CommonTags DESC
