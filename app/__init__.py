# app module
#
# Defines a method create_app() that generates a Flask instance, configures it, and returns it. 
#
# gunicorn calls create_app() and uses the generated Flask instance.

import os
from proxies.TableProxy import TableProxy
from flask import Flask,current_app,Blueprint, request, g
import routes
import blueprints
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from lib.DbHelper import DbHelper,POSTGRES_TYPE
from decouple import config
from werkzeug.exceptions import default_exceptions
from lib.CustomJsonEncoder import CustomJSONEncoder
from lib.DefaultJsonErrorHandler import make_json_error
from json import loads

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)    
    
    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass                    
    
    # Getting config options - this should eventually be in it's own class
    FLASK_SECRET_KEY = config('FLASK_SECRET_KEY')
    pss_db_type = config('pss_db_type',default='postgres')
    pss_db_name = config('pss_db_name') if test_config is None else test_config['pss_db_name']
    pss_db_username = config('db_username')
    pss_db_password = config('db_password')

    # The CORS module is needed because the backend runs on port 8000
    # and the html/javascript is retreived from port 80/443.  The CORS
    # module makes sure the browser/native app doesn't puke with cross site
    # scripting errors when ajax requests are made.
    CORS(
        app,
        allow_headers=['Content-Type', 'Accept'],
        vary_header=False,
        #send_wildcard=False,        
        supports_credentials=True
    )    

    app.db_helper = DbHelper(pss_db_type,pss_db_username,pss_db_password,pss_db_name)    
    db_handle = app.db_helper.create_db_handle(app)        
        
    app.register_blueprint(blueprints.event_bp)     
    app.json_encoder = CustomJSONEncoder                

    app.error_handler_spec[None]={}    
    for code in default_exceptions:        
        app.register_error_handler(code, make_json_error)                                
    app.table_proxy = TableProxy(db_handle,app)        
    app.config['DEBUG']=True
    app.config['SECRET_KEY']=FLASK_SECRET_KEY
    return app
