from typing import Any
from database.db import get_pool
from psycopg.rows import dict_row
from psycopg import errors

def get_user_by_username(username: str) -> dict[str, Any] | None:  
    pool = get_pool()
    with pool.connection() as connection:
        connection.row_factory = dict_row
        with connection.cursor() as cursor:
            cursor.execute('''
                            SELECT user_id, username, hash_pass
                            FROM Users
                            WHERE username = %s
                            ''', [username])
            user = cursor.fetchone()
            if user is None:
                return None
            else:
                return user
            
def get_user_by_user_id(user_id: int) -> dict[str, Any] | None:
    pool = get_pool() 
    with pool.connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute('''
                            SELECT user_id, first_name, last_name, email, username
                            FROM Users
                            WHERE user_id = %s
                            ''', [user_id])
            user = cursor.fetchone()  # Fetch the user by ID
            if user is None:
                return None
            else:
                return user
            
def create_user(first_name : str, last_name : str, email: str, username: str, hashed_password: str):
    pool = get_pool()
    try:
        with pool.connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute('''
                                INSERT INTO Users (first_name, last_name, email, username, hash_pass)
                                VALUES (%s, %s, %s, %s, %s)
                                RETURNING user_id
                                ''', [first_name, last_name, email, username, hashed_password])
                user_id = cursor.fetchone()
                if user_id is None:
                    raise Exception('User not created')
                else:
                    return {'user_id': user_id,
                            'username': username}
    except errors.UniqueViolation as e:
        if 'email' in str(e):
            return{'error': 'Email already exists'}
        elif 'username' in str(e):
            return {'error': 'Username already exists'}
        else:
            raise e
        
            
def create_recipe(recipe_author_id: int, recipe_name: str, recipe_description: str, recipe_ingredients: str, recipe_measurements: str, recipe_instructions: str):
    pool = get_pool()
    with pool.connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute('''
                            INSERT INTO Recipes (recipe_author_id, recipe_name, recipe_description, recipe_ingredients, recipe_measurements, recipe_instructions)
                            VALUES (%s, %s, %s, %s, %s, %s)
                            RETURNING recipe_id
                            ''', [recipe_author_id, recipe_name, recipe_description, recipe_ingredients, recipe_measurements, recipe_instructions])
            recipe_id = cursor.fetchone()
            if recipe_id is None:
                raise Exception('Recipe not created')
            else:
                return recipe_id
            

def get_all_recipes():
    pool = get_pool()
    with pool.connection() as connection:
        connection.row_factory = dict_row
        with connection.cursor() as cursor:
            cursor.execute('''
                            SELECT recipe_id, recipe_author_id, recipe_name, recipe_description, recipe_ingredients, recipe_measurements, recipe_instructions
                            FROM Recipes
                            ''')
            recipes = cursor.fetchall()
            return recipes
        
def get_recipe_id(recipe_name: str) -> int | None:
    pool = get_pool()
    with pool.connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute('''
                            SELECT recipe_id
                            FROM Recipes
                            WHERE recipe_name = %s
                            ''', [recipe_name])
            recipe = cursor.fetchone()
            if recipe is None:
                return None
            else:
                return recipe
            

def delete_recipe(recipe_id: int):
    pool = get_pool()
    with pool.connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute('''
                            DELETE FROM Recipes
                            WHERE recipe_id = %s
                            ''', [recipe_id])
            return None
        
def get_recipe_author_id(user_id: int) -> int | None:
    pool = get_pool()
    with pool.connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute('''
                            SELECT recipe_author_id
                            FROM Recipes
                            WHERE recipe_author_id = %s
                            ''', [user_id])
            recipe_author_id = cursor.fetchone()
            if recipe_author_id is None:
                return None
            else:
                return recipe_author_id
            

def edit_recipe(recipe_id: int, recipe_name: str, recipe_description: str, recipe_ingredients: str, recipe_measurements: str, recipe_instructions: str):
    pool = get_pool()
    with pool.connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute('''
                            UPDATE Recipes
                            SET recipe_name = %s, recipe_description = %s, recipe_ingredients = %s, recipe_measurements = %s, recipe_instructions = %s
                            WHERE recipe_id = %s
                            ''', [recipe_name, recipe_description, recipe_ingredients, recipe_measurements, recipe_instructions, recipe_id])
            return None
            

def delete_recipe(recipe_id: int):
    pool = get_pool()
    with pool.connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute('''
                            DELETE FROM Recipes
                            WHERE recipe_id = %s
                            ''', [recipe_id])
            return None
        
def get_recipe_author_id(user_id: int) -> int | None:
    pool = get_pool()
    with pool.connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute('''
                            SELECT recipe_author_id
                            FROM Recipes
                            WHERE recipe_author_id = %s
                            ''', [user_id])
            recipe_author_id = cursor.fetchone()
            if recipe_author_id is None:
                return None
            else:
                return recipe_author_id
            

def edit_recipe(recipe_id: int, recipe_name: str, recipe_description: str, recipe_ingredients: str, recipe_measurements: str, recipe_instructions: str):
    pool = get_pool()
    with pool.connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute('''
                            UPDATE Recipes
                            SET recipe_name = %s, recipe_description = %s, recipe_ingredients = %s, recipe_measurements = %s, recipe_instructions = %s
                            WHERE recipe_id = %s
                            ''', [recipe_name, recipe_description, recipe_ingredients, recipe_measurements, recipe_instructions, recipe_id])
            return None

def get_recipe_by_name(recipe_name: str):
    pool = get_pool()
    with pool.connection() as connection:
        connection.row_factory = dict_row
        with connection.cursor() as cursor:
            cursor.execute('''
                            SELECT * 
                            FROM Recipes
                            WHERE recipe_name LIKE %s
                            ''', [recipe_name])
                        
            searched_recipes = cursor.fetchall()
            print(searched_recipes)
            if searched_recipes is None:
                raise Exception('Recipe not found')
            else:
                return searched_recipes
