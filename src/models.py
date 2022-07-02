from pony import orm
from os import environ

db_name = environ['PG_DB']
db_user = environ['PG_USER']
db_pass = environ['PG_PASS']

db = orm.Database()
db.bind(provider='postgres', database=db_name, user=db_user, password=db_pass, host='postgresql')
orm.set_sql_debug(True)

class User(db.Entity):
    id = orm.PrimaryKey(int, auto=True)
    name = orm.Required(str)
    email = orm.Required(str)
    password = orm.Required(str)

class Movie(db.Entity):
    id = orm.PrimaryKey(int, auto=True)
    imdb_id = orm.Required(str, unique=True)
    title = orm.Required(str)
    likes_count = orm.Required(int)
    
class Comment(db.Entity):
    id = orm.PrimaryKey(int, auto=True)
    user_id = orm.Required(int)
    movie_id = orm.Required(int)
    comment = orm.Required(str)

db.generate_mapping(create_tables=True)