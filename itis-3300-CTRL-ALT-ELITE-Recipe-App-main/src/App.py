
from flask import Flask, abort, render_template, redirect, url_for, request, session, flash
from app_factory import create_app
from database import database_queries, check_user_sess
from dotenv import load_dotenv


load_dotenv()
app, bcrypt = create_app()

app.secret_key = 'your_secret_key'  # Required for flash messages




#recipes = []  # Storing all the recipes
# users = []  # Storing all users


@app.get('/')
def sign_up():
    return render_template('signup.html')

@app.post('/login')
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    if not username or not password:
        flash("Please enter the required fields")
        return redirect(url_for('login'))
    user = database_queries.get_user_by_username(username)

    if user is None:
        flash("User not found")
        return redirect(url_for('login'))
    if not bcrypt.check_password_hash(user['hash_pass'], password):
        flash("Incorrect password")
        return redirect(url_for('login'))
    session['user_id'] = user['user_id']
    return redirect(url_for('home'))

@app.get('/login')
def log_in():
    return render_template('login.html')

@app.get('/signup')
def sign_up_page():
    return render_template('signup.html')

@app.post('/signup')
def signup():
    first_name = request.form.get('first_name')
    last_name = request.form.get('last_name')
    email = request.form.get('email')
    username = request.form.get('username')
    password = request.form.get('password')
    confirm_password = request.form.get('confirm_password')

    if not first_name or not last_name or not email or not username or not password or not confirm_password:
        flash("Please enter the required fields")
        return redirect(url_for('signup'))
    if password != confirm_password:
        flash("Passwords do not match")
        return redirect(url_for('signup'))
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    user = database_queries.create_user(first_name, last_name, email, username, hashed_password)

    if 'error' in user:
            flash(user['error'])
            return redirect(url_for('signup'))
    flash("Account created successfully, please log in to continue")
    return redirect(url_for('login'))    

@app.route('/home')
@check_user_sess.check_user
def home():
    recipes = database_queries.get_all_recipes()
    return render_template('index.html', recipes=recipes)

@app.get('/logout')
def logout():
    session.clear()
    return redirect(url_for('signup'))


@app.route('/delete_recipe/<int:recipe_id>', methods=['POST'])
def delete_recipe(recipe_id):

    database_queries.delete_recipe(recipe_id)

    
    flash('Recipe successfully deleted!')
    return redirect(url_for('home'))

@app.route('/profile')
@check_user_sess.check_user
def profilePage():
    user_id = session.get('user_id')
    user = database_queries.get_user_by_user_id(user_id)
    return render_template('profile.html', user=user)


@app.route('/recipes')
@check_user_sess.check_user
def recipesPage():
    recipes = database_queries.get_all_recipes()
    return render_template('recipes.html', recipes=recipes)


@app.route('/create-recipe', methods=['GET', 'POST'])
def create_recipe():
    if request.method == 'POST':
        recipe_name = request.form.get('recipe_name')
        recipe_description = request.form.get('recipe_description')
        recipe_ingredients = request.form.get('recipe_ingredients')
        recipe_measurments = request.form.get('recipe_measurements')
        recipe_instructions = request.form.get('recipe_instructions')
        recipe_author_id = session.get('user_id')
        
        if not recipe_name or not recipe_description or not recipe_ingredients or not recipe_instructions:
            flash("Please enter the required fields")
            return redirect(url_for('home'))

        try:
            database_queries.create_recipe(
                recipe_author_id,
                recipe_name,
                recipe_description,
                recipe_ingredients,
                recipe_measurments,
                recipe_instructions
            )
            flash('Recipe created!')
            recipes = database_queries.get_all_recipes()
            print(recipes)
            return render_template('index.html', recipes=recipes)
        except Exception as e:
            flash(f"Error creating recipe: {str(e)}")
        return redirect(url_for('home'))


    

@app.route('/edit_recipe/<int:recipe_id>', methods=['GET', 'POST'])
def edit_recipe(recipe_id):

    if request.method == 'POST':
        recipe_name = request.form['recipe_name']
        recipe_description = request.form['recipe_description']
        recipe_ingredients = request.form['recipe_ingredients']
        recipe_measurements = request.form['recipe_measurements']
        recipe_instructions = request.form['recipe_instructions']
        return redirect(url_for('home'))

    recipe = database_queries.edit_recipe(recipe_id, recipe_name, recipe_description, recipe_ingredients, recipe_measurements, recipe_instructions)


    return render_template('edit_recipe.html', recipe=recipe)



@app.post('/search_recipe')
def search_recipe():
    name = request.form.get('search_name')
    if not name:
        flash("Please enter the required fields")
        return redirect(url_for('home'))
    recipes = database_queries.get_recipe_by_name(name)
    print(recipes)
    if recipes is None:
        flash("No Recipes Found With Entered Name")
    
    return render_template('search_recipe.html', recipes = recipes)


if __name__ == '__main__':
    app.run(debug=True)


# @app.route('/user', methods=['GET', 'POST'])
# def create_user():
#     if request.method == 'POST':
#         # Gets information for new user from request.form statements
#         user = {
#             'id': len(users) + 1,  # Fixed typo here
#             'username': request.form['username'],       
#             'password': request.form['password']
#         }
#         # Adds new user to users dictionary
#         users.append(user)
#         print(users)

#         # Redirects back to the base url for index.html
#         return redirect(url_for('home'))
    
#     # Gets all users
#     return render_template('index.html', users=users)