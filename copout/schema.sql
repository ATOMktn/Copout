DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS post;

CREATE TABLE user (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL
  date_joined DATE NOT NULL,
);

CREATE TABLE post (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  author_id INTEGER NOT NULL,
  created TIMESTAMP NOT NULL,
  title TEXT NOT NULL,
  date_of_inc DATE NOT NULL,
  address TEXT NOT NULL,
  city_of_inc TEXT NOT NULL,
  state_of_inc TEXT NOT NULL,
  lat REAL NOT NULL,
  lng REAL NOT NULL,
  persons TEXT NOT NULL,
  persons_id TEXT NOT NULL,
  org TEXT NOT NULL,
  summary TEXT NOT NULL,
  FOREIGN KEY (author_id) REFERENCES user (id)
);