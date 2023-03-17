from flask_app.config.connection import connectToMySQL
from flask_app.models import user
from flask import flash

class Recipe:
    DB = "recipes_DB"
    def __init__(self, data ):
        self.id = data['id']
        self.user_id = data['user_id']
        self.name = data['name']
        self.description = data['description']
        self.instructions = data['instructions']
        self.under_30 = data['under_30']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_name = None
        
    
    # CRUD METHODS
    
    #CREATE
    @classmethod
    def save_recipe(cls, data):
        query = """
                INSERT INTO recipes 
                ( user_id, name , description , instructions , under_30,  created_at, updated_at ) 
                VALUES 
                ( %(user_id)s, %(name)s , %(description)s , %(instructions)s , %(under_30)s, %(created_at)s , NOW() )
                ;"""
        return connectToMySQL(cls.DB).query_db(query, data)
    
    #READ 
    @classmethod
    def get_all(cls):
        query = """SELECT * 
                FROM recipes
                ;"""
        results = connectToMySQL(cls.DB).query_db(query)
        
        recipes = []
        for row in results:
            recipes.append(cls(row))
        return recipes
    
    #READ ALL 
    @classmethod
    def get_recipes_with_user_name(cls):
        query = """SELECT * 
                FROM recipes
                LEFT JOIN users
                ON recipes.user_id = users.id
                ORDER BY recipes.id DESC
                ;"""
        results = connectToMySQL(cls.DB).query_db(query)
        recipes = []
        for row in results:
            recipe = cls(row)
            user_data = {
                'id': row["users.id"],
                'first_name': row["first_name"],
                'last_name' : row["last_name"],
                'email' : row["email"],
                'password' : '',
                'created_at' : row["created_at"],
                'updated_at' : row["updated_at"], 
                }
            recipe.user_name = user.User(user_data)
            recipes.append(recipe)
        return recipes
        
    #READ ONE 
    @classmethod 
    def get_one(cls, data):
        query = """SELECT * 
                FROM recipes 
                WHERE id = %(id)s
                ;"""
        results = connectToMySQL(cls.DB).query_db( query, data)
        return cls(results[0])
    
    
    @classmethod
    def get_recipe_by_id_with_user_name(cls, data):
        query = """SELECT * 
                FROM recipes
                LEFT JOIN users
                ON recipes.user_id = users.id
                WHERE recipes.id = %(id)s
                ;"""
        results = connectToMySQL(cls.DB).query_db(query, data)
        for row in results:
            recipe = cls(row)
            user_data = {
                'id': row["users.id"],
                'first_name': row["first_name"],
                'last_name' : row["last_name"],
                'email' : row["email"],
                'password' : '',
                'created_at' : row["created_at"],
                'updated_at' : row["updated_at"], 
                }
            recipe.user_name = user.User(user_data)
            print(recipe.user_name.first_name)
        return recipe
    
    
    #UPDATE
    @classmethod
    def update(cls, data):
        query = """
                UPDATE recipes 
                SET first_name = %(name)s, last_name = %(description)s, age = %(intructions)s, updated_at = NOW() 
                WHERE id = %(id)s;
                """
        results = connectToMySQL(cls.DB).query_db(query, data)
        
        return results
    #DELETE
    @classmethod
    def delete(cls, data):
        query = """
                DELETE FROM recipes
                WHERE id = %(id)s;
                """
        results = connectToMySQL(cls.DB).query_db(query, data)
        return results
    
    #VALIDATION
    @staticmethod
    def validate_recipe(recipes):
        is_valid = True
        if len(recipes['name']) < 3:
            flash("Name must be at least 3 characters.")
            is_valid = False
        if len(recipes['description'])  < 8:
            flash("Description must be at least 8 characters.")
            is_valid = False
        if len(recipes['instruction']) < 10:
            flash("Instructions must be at least 10 characters.")
        return is_valid