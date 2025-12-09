

CREATE TABLE IF NOT EXISTS users(
    user_id         SERIAL,   
    first_name      VARCHAR(225)    NOT NULL,   
    last_name       VARCHAR(225)    NOT NULL,   
    email           VARCHAR(225)    NOT NULL UNIQUE, 
    username        VARCHAR(225)    NOT NULL UNIQUE,  
    hash_pass       VARCHAR(225)    NOT NULL,   

    PRIMARY KEY(user_id)
);


CREATE TABLE IF NOT EXISTS recipes(
    recipe_id         SERIAL,
    recipe_author_id  INTEGER         NOT NULL,
    recipe_name      VARCHAR(225)    NOT NULL,
    recipe_description VARCHAR(225)    NOT NULL,
    recipe_ingredients VARCHAR(225)    NOT NULL,
    recipe_measurements VARCHAR(225)    NOT NULL,
    recipe_instructions VARCHAR(225)    NOT NULL,

    PRIMARY KEY (recipe_id),
    FOREIGN KEY (recipe_author_id) REFERENCES users(user_id)
);
