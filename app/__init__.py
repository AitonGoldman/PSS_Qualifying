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
from lib.auth import principal_identity_funcs
from flask_principal import Principal
from flask_login import LoginManager
from werkzeug.exceptions import default_exceptions
from lib.CustomJsonEncoder import CustomJSONEncoder
from lib.DefaultJsonErrorHandler import make_json_error
from json import loads
from flask_marshmallow import Marshmallow
from lib.serialization.PssUserSchema import gen_pss_users_schema

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
    pss_db_name = config('pss_db_name')
    pss_db_username = config('db_username')
    pss_db_password = config('db_password')

    # The CORS module is needed because the backend runs on port 8000
    # and the html/javascript is retreived from port 80/443.  The CORS
    # module makes sure the browser/native app doesn't puke with cross site
    # scripting errors when ajax requests are made.
    CORS(
        app,
        headers=['Content-Type', 'Accept'],
        vary_header=False,
        #send_wildcard=False,        
        supports_credentials=True
    )    

    db_helper = DbHelper(pss_db_type,pss_db_username,pss_db_password,pss_db_name)    
    db_handle = db_helper.create_db_handle(app)        

    LoginManager().init_app(app)

    principals = Principal(app)    
    principal_identity_funcs.generate_pss_user_loader(app)
    principal_identity_funcs.generate_pss_user_identity_loaded(app)
        
    app.register_blueprint(blueprints.event_bp)     
    app.json_encoder = CustomJSONEncoder            
    app.before_request(generate_extract_request_data(app))

    app.error_handler_spec[None]={}
    for code in default_exceptions.iterkeys():        
        app.register_error_handler(code, make_json_error)                            
    app.ma = Marshmallow(app)    
    app.table_proxy = TableProxy(db_handle,app)        
    app.config['DEBUG']=True
    return app

def generate_extract_request_data(app):
    def extract_request_data():
        if request.data:
            g.request_data=loads(request.data)
        else:
            g.request_data = {}
    return extract_request_data