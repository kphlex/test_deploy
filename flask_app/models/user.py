from flask_app import app
from flask_app.config.connection import connectToMySQL
from flask import flash, session, request
import re
from flask_bcrypt import Bcrypt       
bcrypt = Bcrypt(app)

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class User:
    DB = "recipes_DB"
    def __init__(self, data ):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        
    @classmethod
    def save_user(cls, data):
        query = """
                INSERT INTO users 
                (first_name, last_name, email, password, created_at, updated_at)
                VALUES 
                ( %(first_name)s, %(last_name)s , %(email)s , %(password)s , NOW() , NOW() )
                ;"""
        return connectToMySQL(cls.DB).query_db(query, data)
    
    @classmethod
    def get_by_email(cls, data):
        query = """
                SELECT * FROM users
                WHERE email = %(email)s
                ;"""
        result = connectToMySQL(cls.DB).query_db(query, data)
        if len(result) < 1:
            return False
        return cls(result[0])
    
    #VALIDATIONS 
    
    @staticmethod
    def validate_user(user):
        is_valid = True
        #check if user exists 
        data = {
            "email": user['email']
        }
        valid_user = User.get_by_email(data)
        if valid_user:
            flash("Email already in use! Register with a different email or login", 'register')
            is_valid = False
        #Registration Validations
        if len(user['first_name']) < 2:
            flash("First name must be at least 2 characters", 'register')
            is_valid = False
        if len(user['last_name']) < 2:
            flash("Last name must be at least 2 characters", 'register')
            is_valid = False
        if not EMAIL_REGEX.match(user['email']):
            flash('Invalid email address', 'email', 'register')
            is_valid = False
        if len(user['password']) < 8:
            flash('Password must be at least 8 characters', 'register')
            is_valid = False
        if not any(char.isdigit() for char in user['password']):
            flash('Password must contain at least one number', 'register')
            is_valid = False
        if not any(char.isupper() for char in user['password']):
            flash('Password must contain at least one uppercase letter', 'register')
            is_valid = False
        if user['conf_password'] != user['password']:
            flash('Password does not match.', 'register')
            is_valid = False
        return is_valid
    
    #Login validations 
    @staticmethod
    def validate_login(user):
        if 'attempt' not in session:
            session['attempt'] = 5
        is_valid = True
        data = {
            "email" : user['email']
        }
        valid_user = User.get_by_email(data)
        if not valid_user:
            if session['attempt'] == 1:
                client_ip= session.get('client_ip')
                flash('This is your last attempt, %s will be blocked for 24hr, Attempt %d of 5'  % (client_ip,session['attempt']), 'login')
            else:
                flash('Invalid login credentials, Attempts %d of 5'  % session['attempt'], 'login')
                is_valid = False
        if not bcrypt.check_password_hash(valid_user.password, user['password']):
            if session['attempt'] == 1:
                client_ip= request.remote_addr
                flash('This is your last attempt,IP Address %s will be blocked for 24hr, Attempt %d of 5'  % (client_ip, session['attempt']), 'login')
                is_valid = False
            if session['attempt'] == 0:
                session.clear()
                print('this works')
                is_valid = False
            else:
                flash('Invalid login credentials, Attempts %d of 5' % session['attempt'], 'login')
                session['attempt'] -= 1   
                print(session['attempt'])
                is_valid = False
        return is_valid