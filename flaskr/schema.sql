CREATE TABLE tracks (
    id INT PRIMARY KEY,
    title VARCHAR(255),
    artist VARCHAR(255),
    genre VARCHAR(255),
    length INT
);

CREATE TABLE genres (
    id INTEGER PRIMARY KEY,
    title TEXT
);