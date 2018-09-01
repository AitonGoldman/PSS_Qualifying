import os
from flask import Flask, request, g
import routes
import blueprints
from flask_cors import CORS
from lib.DbHelper import DbHelper
from decouple import config
from lib.auth import principal_identity_funcs
from flask_principal import Principal
from flask_login import LoginManager
from werkzeug.exceptions import default_exceptions
from lib.CustomJsonEncoder import CustomJSONEncoder
from lib.DefaultJsonErrorHandler import make_json_error
from json import loads
from flask_marshmallow import Marshmallow

def create_app(test_config=None):    
    app = Flask(__name__, instance_relative_config=True)    
    app.ma = Marshmallow(app)        
        
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

    LoginManager().init_app(app)

    principals = Principal(app)    
    principal_identity_funcs.generate_pss_user_loader(app)
    principal_identity_funcs.generate_pss_user_identity_loaded(app)
    
    app.register_blueprint(blueprints.event_bp)     
    app.json_encoder = CustomJSONEncoder                
    app.before_request(generate_extract_request_data(app))

    app.error_handler_spec[None]={}    
    for code in default_exceptions:        
        app.register_error_handler(code, make_json_error)                                
    app.config['DEBUG']=True
    app.config['SECRET_KEY']=FLASK_SECRET_KEY
    return app

def generate_extract_request_data(app):
    def extract_request_data():                
        if request.data:            
            g.request_data=loads(request.get_data(as_text=True))
        else:            
            g.request_data = {'poop':'shoop'}
    return extract_request_data
