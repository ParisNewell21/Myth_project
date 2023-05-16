from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash 
from flask_app.models import creature, creature

class Story:

    db= 'mythdb2' 

    def __init__( self , data ):
        self.id = data['id']
        self.story_name = data['story_name']
        self.content = data['content']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.watcher = None


##########CREATE#############
    @classmethod
    def add_story(cls, data):
        query = """insert into story( story_name, content, created_at, updated_at, creature_id )
        values ( %(story_name)s, %(content)s, NOW(), NOW(), %(creature_id)s );"""
        return connectToMySQL(cls.db).query_db(query, data)

#########DELETE##############
    @classmethod
    def delete(cls, data):
        query  = "delete from story where id = %(id)s;"
        return connectToMySQL(cls.db).query_db(query,data)
    #do I need to?

#########UPDATE############
    @classmethod
    def update_story(cls,data):
        query = """UPDATE story
        SET story_name=%(story_name)s, content= %(content)s, updated_at=NOW() 
        WHERE id = %(id)s;"""
        return connectToMySQL(cls.db).query_db(query,data)

############READ############

    @classmethod
    def get_all(cls):
        query = """ SELECT * FROM story
                    LEFT JOIN creature on creature.id = story.creature_id;"""
        results = connectToMySQL(cls.db).query_db(query)
        print(results)
        storys=[]
        for row in results:
            for key in row.keys():
                print(key)
            this_story = cls(row)
            creature_data = {
                'id': row['creature.id'],
                'first_name': row['first_name'],
                'last_name': row['last_name'],
                'email': row['email'],
                'password': "",
                'created_at': row['creature.created_at'],
                'updated_at': row['creature.updated_at']
            }
            this_story.watcher = creature.creature(creature_data)
            storys.append(this_story)
        return storys
    #cls=dictionary row = row in dictionary this already has tree data so you need to add creature data to the left join 


    @classmethod
    def get_one(cls,data):
        query = """
                SELECT * FROM story
                JOIN creature on story.creature_id = creature.id
                WHERE story.id = %(id)s;
                """
        result = connectToMySQL(cls.db).query_db(query,data)
        if not result:
            return False
        result = result[0]
        this_story = cls(result)
        creature_data = {
                "id": result['creature.id'],
                "first_name": result['first_name'],
                "last_name": result['last_name'],
                "email": result['email'],
                "password": "",
                "created_at": result['creature.created_at'],
                "updated_at": result['creature.updated_at']
        }
        this_story.watcher = creature.creature(creature_data)
        return this_story

##########static#########

    @staticmethod
    def validate_story(data):
        is_valid = True
        if len(data['story_name']) < 2:
            flash("A name is needed","stop")
            is_valid = False
        if len(data ['content']) <3:
            flash("You don't want to talk about it?","stop")
            is_valid = False 
        return is_valid

