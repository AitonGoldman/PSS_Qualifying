# Set the following env variables if env variable "DATABASE_TYPE" is "pg" : 
# DB_USERNAME : the username for the postgres database
# DB_PASSWORD : the password for the postgres database user
# DB_NAME : the name of the existing postgres database

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlathanor import FlaskBaseModel, initialize_flask_sqlathanor
import os

def generate_event_model(db):
    class Events(db.Model):
        event_id = db.Column(db.Integer, primary_key=True, supports_json = True)
        event_name = db.Column(db.String(80), unique=True, nullable=False, supports_json = True)                
        event_settings_values = db.relationship("EventSettingsAssociation",lazy="joined", supports_json = True)        
        def __repr__(self):
            return '<Event %r>' % self.event_name        
    return Events

def generate_event_settings_association_model(db):    
    class EventSettingsAssociation(db.Model):        
        event_id = db.Column(db.Integer, db.ForeignKey('events.event_id'), primary_key=True, supports_json = True)        
        extra_data = db.Column(db.String(50), supports_json = True)                
    return EventSettingsAssociation

if os.environ.get('DB_TYPE',None) == "pg":
    db_url="postgresql://%s:%s@localhost/%s" % (os.environ['DB_USERNAME'],os.environ['DB_PASSWORD'],os.environ['DB_NAME'])
else:
    db_url="sqlite:////tmp/test.db"
    
app = Flask(__name__, instance_relative_config=True)
app.config['SQLALCHEMY_DATABASE_URI'] = db_url
db_handle = SQLAlchemy(app,model_class = FlaskBaseModel)        
db_handle = initialize_flask_sqlathanor(db_handle)
events = generate_event_model(db_handle)
event_settings_association = generate_event_settings_association_model(db_handle)
json_passes = '{"event_name":"testing_event","event_settings_values":[]}'
print(events.new_from_json(json_passes))
json_fails = '{"event_name":"testing_event","event_settings_values":[{"extra_data":"test_data"}]}'
print(events.new_from_json(json_fails))
    
