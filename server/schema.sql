DROP TABLE IF EXISTS client;
DROP TABLE IF EXISTS vote;
DROP TABLE IF EXISTS user;

CREATE TABLE client (
  client_id INTEGER PRIMARY KEY AUTOINCREMENT,
  client TEXT UNIQUE NOT NULL,
  token TEXT NOT NULL,
  token_start CHAR(3) NOT NULL,
  location_id INTEGER NOT NULL /* external location id */
);

CREATE TABLE vote (
  vote_id INTEGER PRIMARY KEY AUTOINCREMENT,
  client_id INTEGER NOT NULL,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  upvote BOOLEAN NOT NULL,
  FOREIGN KEY (client_id) REFERENCES client (client_id)
);

CREATE TABLE user(
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT UNIQUE NOT NULL,
    role TEXT UNIQUE NOT NULL DEFAULT 'user'
);