# import the function that will return an instance of a connection
import re
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 
PW_UPPER = re.compile(r'^.*[A-Z]+.*$')
PW_NUMBER = re.compile(r'^.*[0-9]+.*$')
# model the class after the friend table from our database
class User:
    def __init__( self , data ):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
# Now we use class methods to query our database
    @staticmethod
    def validate_user( user ):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        is_valid = True
        # test whether a field matches the pattern
        if not EMAIL_REGEX.match(user['email']): 
            flash("Invalid email address!", "register")
            is_valid = False
        if len(user['fname']) < 1:
            flash("First Name must be at least 1 character.", "register")
            is_valid = False
        if len(user['lname']) < 1:
            flash("Last Name must be at least 1 character.", "register")
            is_valid = False
        if len(user['pw']) < 3:
            flash("Password must be at least 3 characters.", "register")
            is_valid = False
        if len(connectToMySQL('user_login').query_db(query,user))>0:
            flash("This email is already registered in our database.", "register")
            is_valid=False
        if not PW_UPPER.match(user['pw']) or not PW_NUMBER.match(user['pw']):
            flash("Your password must have at least 1 number and 1 upper case letter", "register")
            is_valid = False
        if user['pw'] != user['cpw']:
            flash("Your password does not match the password confirmed", "register")
            is_valid = False
        return is_valid
    @staticmethod
    def validate_login( user ):
        is_valid = True
        # test whether a field matches the pattern
        if not EMAIL_REGEX.match(user['email']): 
            flash("Invalid email address!", "login")
            is_valid = False
        if len(user['pw']) < 3:
            flash("Password must be at least 3 characters.", "login")
            is_valid = False
        return is_valid
    @classmethod
    def login(cls,data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        # make sure to call the connectToMySQL function with the schema you are targeting.
        user = connectToMySQL('user_login').query_db(query,data)
        if len(user) <1:
            flash("The email provided does not belong to any of our users. Please register", "login")
            return False
        print(user)
        return cls(user[0])
    @classmethod
    def get_user_info(cls,data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        # make sure to call the connectToMySQL function with the schema you are targeting.
        user = connectToMySQL('user_login').query_db(query,data)
        return cls(user[0])
    @classmethod
    def save(cls, data ):
        query = "INSERT INTO users ( first_name , last_name , email , password, created_at, updated_at ) VALUES ( %(first_name)s , %(last_name)s , %(email)s ,%(password)s, NOW() , NOW() );"
        # data is a dictionary that will be passed into the save method from server.py
        return connectToMySQL('user_login').query_db( query, data )
