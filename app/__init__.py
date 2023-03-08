from flask import Flask
import os
from sqlobject import *
from .routes.index import root
from .routes.books import books
from .routes.members import members
from .routes.transactions import transaction
from .models.books import Books
from .models.members import Members
from .models.transactions import Transactions
from flask_cors import CORS
def create_app(mode):
    app=Flask(__name__)
    if(mode=="development"):
        db_filename = os.path.abspath('library.sqlite')
        connection_string = 'sqlite:' + db_filename
        connection = connectionForURI(connection_string)
        sqlhub.processConnection = connection
    elif(mode=="testing"):
        db_filename = os.path.abspath('testing.sqlite')
        connection_string = 'sqlite:' + db_filename
        connection = connectionForURI(connection_string)
        sqlhub.processConnection = connection
    CORS(app)
    Books.createTable(ifNotExists=True)
    Members.createTable(ifNotExists=True)
    Transactions.createTable(ifNotExists=True)
    app.register_blueprint(root)
    app.register_blueprint(books,url_prefix='/book')
    app.register_blueprint(members,url_prefix='/member')
    app.register_blueprint(transaction,url_prefix='/transaction')
    return app