# DbHelper.py
#
# What it says on the tin.  Helper class for dealing with the database.  
#
from sqlalchemy_utils import create_database, database_exists, drop_database as sql_utils_drop_database
from flask_sqlalchemy import SQLAlchemy
from proxies.TableProxy import TableProxy

POSTGRES_TYPE='postgres'
SQLITE_TYPE='sqlite'

# DbHelper
#
# Arguments to the class __init__() are everything needed to connect to a db 
class DbHelper():    
    def __init__(self,
                 db_type,
                 db_username,
                 db_password,
                 db_name,
                 db_host_and_port=None):
        if db_name is None:
            raise Exception('tried to create DbHelper without db name')
        if db_type is POSTGRES_TYPE and (db_username is None or db_password is None):            
            raise Exception('tried to create DbHelper without enough connection information')
        if db_type in [POSTGRES_TYPE,SQLITE_TYPE]:
            self.db_type = db_type
        else:
            raise Exception('Unknown type of database passed into DbHelper contructor')
        self.db_username=db_username
        self.db_password=db_password
        self.db_name=db_name
        
        if db_host_and_port:
            self.db_host=db_host_and_port
        else:
            self.db_host='localhost'

    # generate_db_url
    #
    # generate a sqlalchemy connection url based on info the DbHelper has
    def generate_db_url(self):
        if self.db_type == SQLITE_TYPE:
            db_url= "sqlite:////tmp/%s.db" % self.db_name    
        if self.db_type == POSTGRES_TYPE:
            db_url="postgresql://%s:%s@localhost/%s" % (self.db_username,self.db_password,self.db_name)
        return db_url

    # check_database_exists()
    #
    # what it says on the tin
    def check_database_exists(self):        
        db_url = self.generate_db_url()
        return database_exists(db_url)
        
    # create_db_handle()
    #
    # creates a SQLAlchemy instance based on info the DbHelper has, and returns it
    def create_db_handle(self,flask_app,debug=False):
        flask_app.config['SQLALCHEMY_DATABASE_URI'] = self.generate_db_url()    
        flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        if debug:
            app.config['SQLALCHEMY_ECHO']=True
        db_handle = SQLAlchemy(flask_app)
        return db_handle

    # create_db_and_tables
    #
    # creates the database based on the database_name member of the class
    # and then creates the tables based on Models that TableProxy knows about
    def create_db_and_tables(self, app, drop_tables=False):            
        db_url = self.generate_db_url()                
        if not database_exists(db_url):
            create_database(db_url)
        db_handle = self.create_db_handle(app)
        #if self.db_type == POSTGRES_TYPE:
        #    self.check_if_ranking_funcs_exists(db_handle)        
        app.tables = TableProxy(db_handle)        
        self.create_tables(db_handle, drop_tables=drop_tables)
        db_handle.engine.dispose()                                                     
    
    def create_tables(self, db_handle,drop_tables=False):
        db_handle.reflect()
        if drop_tables:
            db_handle.drop_all()
            db_handle.session.commit()
        db_handle.create_all()    
        
