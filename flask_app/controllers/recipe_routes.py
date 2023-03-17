from flask_app import app
from flask import render_template, redirect, request, session
from flask_app.models import recipes

# CRUD METHODS

#Create
@app.route('/create')
def create_form():
    return render_template('create.html')


@app.route('/create/recipe', methods=['POST'])
def create_recipe():
    recipes.Recipe.save_recipe(request.form)
    return redirect('/dashboard')

#Read
@app.route('/recipe/show/<int:id>')
def show_one(id):
    data = {
        'id': id
    }
    return render_template('show_recipe.html', recipe = recipes.Recipe.get_recipe_by_id_with_user_name(data))

#Update
@app.route('/recipe/edit/<int:id>')
def edit(id):
    data = {
        'id': id
    }
    return render_template('edit_recipe.html', recipe = recipes.Recipe.get_one(data))


@app.route('/recipe/update', methods = ['POST'])
def update():
    updated_id = request.form['id']
    recipes.Recipe.update(request.form)
    return redirect(f'/recipe/show/{updated_id}')

#Delete
@app.route('/recipe/delete/<int:id>')
def delete(id):
    data = {
        'id': id
    }
    recipes.Recipe.delete(data)
    return redirect('/dashboard')