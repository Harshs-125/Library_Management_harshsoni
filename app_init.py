from flask import Flask
import os
from constants import SQL_DATABASE_URL
from sqlobject import *
from routes.index import root
from routes.books import books
from models.books import Books
from constants import SQL_DATABASE_URL
def app_init():

    app=Flask(__name__)
    db_filename = os.path.abspath('library.sqlite')
    connection_string = 'sqlite:' + db_filename
    # print(connection_string)
    connection = connectionForURI(connection_string)
    sqlhub.processConnection = connection
    Books.createTable(ifNotExists=True)
    app.register_blueprint(root)
    app.register_blueprint(books,url_prefix='/book')
    return app 
    