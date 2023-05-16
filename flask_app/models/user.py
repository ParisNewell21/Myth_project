from flask_app.config.mysqlconnection import connectToMySQL
import re   
from flask_app.models import creature
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 
from flask import flash 

#need to be able to add to user column and grab one for later

class User:
    db = 'mythdb2'

    def __init__( self , data ):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.liked_creatures = []



#########################login/register###################
    @classmethod
    def save(cls, data):
        query = "insert into user (first_name, last_name, email, password, created_at, updated_at) values ( %(first_name)s, %(last_name)s, %(email)s, %(password)s, NOW(), NOW() );"
        return connectToMySQL(cls.db).query_db(query, data)
    #register

    @classmethod
    def get_by_email(cls,data):
        query = "select * from user where email = %(email)s;"
        results = connectToMySQL(cls.db).query_db(query,data)
        if len(results) < 1:
            return False
        return cls(results[0])


    @classmethod
    def get_by_id(cls,data):
        query = "select * from user where id = %(id)s;"
        results = connectToMySQL(cls.db).query_db(query,data)
        return cls(results[0])
    #pull id



############################################static############################################

    @staticmethod
    def validate_user(data):
        is_valid = True
        if len(data ['first_name']) < 2:
            flash(" Your first name must be at least 2 characters","reg")
            is_valid = False
        if len(data ['last_name']) <2:
            flash("Your Last name must be at least 2 characters","reg")
            is_valid = False 
        if not EMAIL_REGEX.match(data ['email']):
            flash('Your email is invalid', "reg")
            is_valid = False
        if len(data['password']) < 8:
            flash("Password must be at least 8 characters","reg")
            is_valid = False
        if data['password'] != data['confirm']:
            flash("Passwords don't match","reg")
            is_valid = False
        return is_valid


################likes###############

    @classmethod
    def add_likes(cls,data):
        query = "INSERT INTO likes (user_id,creature_id) VALUES (%(user_id)s,%(creature_id)s);"
        return connectToMySQL(cls.db).query_db(query,data)


    @classmethod
    def get_like_id(cls,data):
        query = "SELECT * FROM user LEFT JOIN likes ON user.id = likes.user_id LEFT JOIN creature ON creature.id = likes.creature_id WHERE user.id = %(id)s;"
        results = connectToMySQL(cls.db).query_db(query,data)

        # Creates instance of user object from row one
        user = cls(results[0])
        # append all creature objects to the instances likes list.
        for row in results:
            # if there are no likes
            if row['creature.id'] == None:
                break
            # common column names come back with specific tables attached
            data = {
                "id": row['creature.id'],
                "creature_name": row['creature_name']
            }
            user.liked_creatures.append(creature.Creature(data))
        return user
