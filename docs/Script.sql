CREATE TABLE client (
    client_id INTEGER,
    client TEXT NOT NULL,
    token TEXT NOT NULL,
    token_start CHAR(3) NOT NULL,
    location_id INTEGER NOT NULL,
    PRIMARY KEY (client_id),
    UNIQUE (client)
);
CREATE TABLE vote (
    vote_id INTEGER,
    client_id INTEGER NOT NULL,
    created TIMESTAMP DEFAULT (CURRENT_TIMESTAMP) NOT NULL,
    upvote BOOLEAN NOT NULL,
    PRIMARY KEY (vote_id),
    FOREIGN KEY(client_id) REFERENCES client (client_id)
);
CREATE TABLE user (
    user_id INTEGER,
    username TEXT NOT NULL,
    password_hash TEXT NOT NULL,
    role TEXT DEFAULT 'user' NOT NULL,
    PRIMARY KEY (user_id),
    UNIQUE (username)
);
CREATE VIEW vote_daily AS
SELECT SUM(
        CASE
            WHEN v.upvote THEN 1
            ELSE 0
        END
    ) as upvotes,
    SUM(
        CASE
            WHEN v.upvote THEN 0
            ELSE 1
        END
    ) as downvotes,
    DATE(v.created) as 'date',
    c.location_id
FROM vote v
    INNER JOIN client c on c.client_id = v.client_id
GROUP BY 3,
    4;