from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash 
from flask_app.models import user

class Creature:

    db= 'mythdb2' 

    def __init__( self , data ):
        self.id = data['id']
        self.creature_name = data['creature_name']
        self.watcher = None


##########CREATE#############
    @classmethod
    def add_creature(cls, data):
        query = """insert into creature ( creature_name )
        values ( %(creature_name)s;"""
        return connectToMySQL(cls.db).query_db(query, data)

#########DELETE##############
    @classmethod
    def delete(cls, data):
        query  = "delete from creature where id = %(id)s;"
        return connectToMySQL(cls.db).query_db(query,data)
    #do I need to?

#########UPDATE############
    @classmethod
    def update_creature(cls,data):
        query = """UPDATE creature
        SET creature_name=%(creature_name)s, updated_at=NOW() 
        WHERE id = %(id)s;"""
        return connectToMySQL(cls.db).query_db(query,data)

############READ############

    @classmethod
    def get_all(cls):
        query = """ SELECT * FROM stories
                    LEFT JOIN creature on creature.id = stories.creature_id;"""
        results = connectToMySQL(cls.db).query_db(query)
        print(results)
        creatures=[]
        for row in results:
            for key in row.keys():
                print(key)
            this_creature = cls(row)
            user_data = {
                'id': row['user.id'],
                'first_name': row['first_name'],
                'last_name': row['last_name'],
                'email': row['email'],
                'password': "",
                'created_at': row['user.created_at'],
                'updated_at': row['user.updated_at']
            }
            this_creature.watcher = user.User(user_data)
            creatures.append(this_creature)
        return creatures
    #cls=dictionary row = row in dictionary this already has tree data so you need to add user data to the left join 


    @classmethod
    def get_one(cls,data):
        query = """
                SELECT * FROM creature
                JOIN user on creature.user_id = user.id
                WHERE creature.id = %(id)s;
                """
        result = connectToMySQL(cls.db).query_db(query,data)
        if not result:
            return False
        result = result[0]
        this_creature = cls(result)
        user_data = {
                "id": result['user.id'],
                "first_name": result['first_name'],
                "last_name": result['last_name'],
                "email": result['email'],
                "password": "",
                "created_at": result['user.created_at'],
                "updated_at": result['user.updated_at']
        }
        this_creature.watcher = user.User(user_data)
        return this_creature

##########static#########

    @staticmethod
    def validate_creature(data):
        is_valid = True
        if len(data['creature_name']) < 2:
            flash("A name is needed","stop")
            is_valid = False
        if len(data ['content']) <3:
            flash("You don't want to talk about it?","stop")
            is_valid = False 
        return is_valid


