from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models.user import User
from flask_app.models import recipes
from flask_bcrypt import Bcrypt        
bcrypt = Bcrypt(app)



@app.route('/')
def index():
    return render_template('login.html')

@app.route('/register/user', methods=['POST'])
def register():
    if not User.validate_user(request.form):
        session['first_name'] = request.form['first_name']
        session['last_name'] = request.form['last_name']
        session['email'] = request.form['email']
        return redirect('/')
    else:
        session.clear()
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    print(pw_hash)
    data = {
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['email'],
        "password": pw_hash,
        }
    user_id = User.save_user(data)
    session['user_id'] = user_id
    return redirect('/')


@app.route('/login/user', methods=['POST'])
def login():
    data = {
        'email': request.form['email']
    }
    user_in_db = User.get_by_email(data)
    if not User.validate_login(request.form):
        return redirect('/')
    session['user_id'] = user_in_db.id
    session['first_name'] = user_in_db.first_name
    session['last_name'] = user_in_db.last_name
    return redirect('/dashboard')


@app.route('/dashboard')
def dashboard():
    if not session:
        return redirect('/')
    recipe_list = recipes.Recipe.get_recipes_with_user_name()
    return render_template('dashboard.html', recipe_list = recipe_list)

@app.route('/logout')
def logout_user():
    session.clear()
    return redirect('/')


@app.errorhandler(404)
def invalid_request(e):
    return ('WHO GOES THERE!!!!')