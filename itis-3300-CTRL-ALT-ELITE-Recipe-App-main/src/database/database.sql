CREATE TABLE users_recipe_books (
	user_id			 AUTO_INCREMENT,
	username			 varchar(512) NOT NULL,
	password			 varchar(512) NOT NULL,
	recipe_books_recipebook_id NOT NULL AUTO_INCREMENT,
	recipe_books_num_recipes	 numeric(8,2) DEFAULT 0,
	PRIMARY KEY(user_id)
);

CREATE TABLE recipes (
	recipe_id			 AUTO_INCREMENT,
	recipe_name		 varchar(512),
	recipe_description	 varchar(512),
	recipe_ingredients	 varchar(512),
	recipe_measurements varchar(512),
	recipe_instructions	 varchar(512),
	users_recipe_books_user_id int NOT NULL,
	PRIMARY KEY(recipe_id)
);

CREATE TABLE tokens (
	token			 varchar(512),
	username			 varchar(512),
	timeout			 timestamp,
	users_recipe_books_user_id int NOT NULL,
	PRIMARY KEY(token)
);

ALTER TABLE users_recipe_books ADD UNIQUE (username, recipe_books_recipebook_id);
ALTER TABLE recipes ADD CONSTRAINT recipes_fk1 FOREIGN KEY (users_recipe_books_user_id) REFERENCES users_recipe_books(user_id);
ALTER TABLE tokens ADD UNIQUE (users_recipe_books_user_id);
ALTER TABLE tokens ADD CONSTRAINT tokens_fk1 FOREIGN KEY (users_recipe_books_user_id) REFERENCES users_recipe_books(user_id);