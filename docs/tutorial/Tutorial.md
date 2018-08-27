# Setup and Installation

## Pre-reqs (Estimated time to complete : 10-15 minutes)
You can do one of the following things to get the pre-reqs installed
- [Install the needed packages on your Linux ubuntu machine or OS X machine](LocalInstall.md)
- If you don't want to install the needed packages or you are on a windows machines [download an existing VirtualBox image](VirtualBoxAppliance.md) with everything installed and configured 
- If you don't want to download the 1 gig existing VM image, you can [create and configure a VM on your own](CreateVmFromScratch.md) 
 
## Overview

Please see the architecture document [here](../arch/README.md) before continuing.  Once you have read the overview, please checkout the branch `tutorial_part_1`.
 
The code in this branch will be a minimum skeleton to demonstrate how PSS_Qualifying works.  The skeleton has implemented one feature : allowing users to get information about a specific `Event`. This tutorial uses the skeleton to introduce you to the PSS_Qualifying code structure and how it works.
 
## A quick demo
Before we start the tutorial, let's try using the skeleton to get information about the event that was inserted into the database by the bootstrapping script.  We do this by running the following command at the top level of the PSS_Qualifying repo : 
```
PYTHONPATH=. gunicorn -b 0.0.0.0:8000 'test_app:create_app' -w $1 --reload
```
You have now started the PSS_Qualifying server.   In order to use the PSS_Qualifying server to get the info for the existing event in the database, hit the url `http://0.0.0.0:8000/event/1` (in a seperate shell with `curl` or through your webbrowser) and you will get the event info that looks like this : 
```
 {
   event_id:1,
   event_name:"test"
 }
```
     
A quick explanation of what just happened : Gunicorn is a WSGI HTTP Server - which means it will handle accepting incoming HTTP requests.  Gunicorn needs to be told where the code is that will handle processing HTTP requests - the `test_app:create_app` argument points gunicorn to the Flask object that is configured by our code.  When you hit the `http://0.0.0.0:8000/event/1` url, the Flask object handles routing the request to the appropriate code that processes the request. 
     
The rest of this document covers how information is stored in the database, how that information is accessed by the PSS_Qualifying code, and how that information gets requested by (and returned to) users.
     
     
## Directory structure of PSS_Qualifying
     
- app : The code that initializes and configures the Flask object lives here.
- ignore : a directory that will be ignored by git ( good for putting secret info into ).
- lib : Code that is shared across PSS_Qualifying goes here.
- models : The SQLalchemy models live here.
- proxies : The code that is responsible for accessing the database lives here.
- routes : The code that implements the business logic as Flask routes lives here.
- tests : Unit and integration tests live here.
- utils : Scripts that are needed for bootstrapping, starting the PSS_Qualifying server, and dumping info from the databases live here.

## Flask configuration
Please read the following parts of the flask QuickStart before continuing - they will explain Flask routes and Flask blueprints (FIXME).

Now let's look at the code in `app/__init__.py` which handles configuring the Flask object at startup and is called by gunicorn :
```
import routes
from flask_sqlalchemy import SQLAlchemy
import blueprints
from decouple import config

def create_app(test_config=None):

  FLASK_SECRET_KEY = config('FLASK_SECRET_KEY')  
  db_name = config('pss_db_name') if test_config is None else test_config['pss_db_name']
  db_username = config('db_username')
  db_password = config('db_password')

  app = Flask(__name__, instance_relative_config=True)    
  app.config['SECRET_KEY']=FLASK_SECRET_KEY
  
  db_url="postgresql://%s:%s@localhost/%s" % (db_username,db_password,db_name)
  app.config['SQLALCHEMY_DATABASE_URI'] = db_url

  SQLAlchemy_handle = SQLAlchemy(app)
  app.table_proxy = TableProxy(SQLAlchemy_handle,app)                  

  app.register_blueprint(blueprints.event_bp)     

  return app
```

`create_app()` returns a configured Flask object that will be used by gunicorn for routing requests.

The `create_app()` code highlighted above creates an instance of a Flask object, then creates an instance of a SQLAlchemy object, then creates an instance of TableProxy and put it inside the Flask object, and then registers the `event_bp` blueprint with the Flask instance.

The skeleton uses the `config()` method from the `decouple` module to retrieve environment variables.  It is only used for getting environment variables in the skeleton, but it allows for much more advanced configuration management ( see here for docs - FIXME).

All Flask routes for PSS_Qualifying are placed in the `routes` directory, and all .py files in the directory are imported at the module level (see `routes/__init__.py`).  The end result is that the `import routes` line imports all the route definitions.  When the Flask object is created it detects the imported routes and uses them.

The SQLAlchemy object comes from the Flask-sqlalchemy package ( docs here ).  The object does many things ( and will be discussed in more detail later ) but for now it represents a connection to a database. 

The `TableProxy` instance is what is used by the business logic code ( i.e. the routes ) to access the database, and will be discussed in more detail later.

PSS_Qualifying uses Flask blueprints for declaring routes.  In this skeleton we are only registering one blueprint and not using any of the features of blueprints, but we will be using more blueprints and their feature in the master branch.
    
Now let's look at the route that got used during our quick demo

## Event route

The route is defined in `routes/event.py` Let's take a look at it :

```
from blueprints import event_bp
from flask import current_app,jsonify
from flask_restless.helpers import to_dict
from werkzeug.exceptions import BadRequest, Unauthorized, NotFound

def get_event(table_proxy):
  event, dict_to_return = table_proxy.events_proxy.get_event(event_id=event_id)
  if event is None:
    raise NotFound("Invalid event id")
  return dict_to_return

@event_bp.route('/event/<int:event_id>', methods=["GET"])
def get_event_route(event_id):                    
  dict_to_return = get_event(current_app.table_proxy) 
  return jsonify({'data':dict_to_return}) 

```
The decorator for `get_event_route()` tells Flask which url maps to it - specifically any request url that matches `/event/<int>` where <int> is an integer.

`get_event_route()` calls `get_event()` which is what is responsible for getting the event from the database by it's event_id.  `get_event_route()` passes `get_event()` the `TableProxy` that was created when the Flask instance was configured.  It gets the `TableProxy` from  `current_app` which is what it says on the tin  - it's the current Flask instance ( ie the instance that called `get_event_route()` ).

`get_event_route()` takes the results of `get_event()` (a dict representing the found SQLAlchemy Event object) and `jsonify`-ies it and returns the result.  `jsonify()` takes a dict, converts it to a json string, and then creates a `HTTP Response` (link to http response - FIXME) with the json string as the body of the response.   All Flask routes must return a `HTTP Response` or raise a http exception.

`get_event()` uses the `TableProxy` instance - specifically the `EventsProxy` contained in the `TableProxy` - to retrieve the `Event` by the event_id.

If no event is found, a `BadRequest` exception is raised.  In this case, the exception will rise up the stack until Flask converts it to a 400 http response with the body "Invalid event id".  All code should follow this pattern of raising http exceptions when problems are encountered (see here for list of http exceptions - FIXME) 

`get_event()` is a separate function from `get_event_route()` - it is separate because it allows us to easily unit test the business logic.  Because the `TableProxy` is an argument to `get_event()`, it is easy to mock it and thus test `get_event()`.  All code should follow this pattern : seperate the business logic from the functions that are decorated as Flask routes, and pass any "global" variables into the functions that implements the business logic.

Now let's dig into the `TableProxy` and `EventsProxy` and see how they work...

## TableProxy and EventsProxy
                                          
The `TableProxy` class is in `proxies/TableProxy.py`.  Let's look at the `__init__()` function :
                                                     
```
def __init__(self, sqlAlchemyHandle, app):
  self.sqlAlchemyHandle = sqlAlchemyHandle
  self.events_proxy = EventsProxy(self.sqlAlchemyHandle)
```
                                                                             
It takes a `SQLalchemy` object as an argument (the `sqlAlchemyHandle` is expected to be the `SQLalchemy` object created in `app/__init__.py`).  The `TableProxy` creates an instance of the `EventsProxy` class in it's `__init__()` function.  The `EventsProxy` contains all the code related to accessing the `Events` table in the database.  Note that each table in the database will have it's own Proxy class.  

Let's take a look at the `EventsProxy` class in `proxies/EventsProxy.py`, and let's start with the `__init__()` function :
                                                                             
```
def __init__(self,
             sqlAlchemyHandle,
             event_model=None):
    self.sqlAlchemyHandle = sqlAlchemyHandle
    self.event_model=generate_event_model(self.sqlAlchemyHandle)
```
                                                                                                                                   
The `__init__()` function will call `generate_event_model()` which generates a SQLAlchemy model class.  A SQLAlchemy models represent a table in the database and is used to run queries against the database for that table.  For more information on SQLAlchemy models and how they get used, look at the SQLAlchemy ORM tutorial ( FIXME : link here )

Now let's look at the `get_event()` function and how it uses the SQLAlchemy model class : 

```
def get_event(self,event_id,serialized=True):
  event = self.event_model.query.filter_by(event_id=event_id).first()
  if serialized:                                                                                                                                           if event is None:
      return None,None
    dict_to_return = to_dict(event)
    return event,dict_to_return
  else:
    return event 
```

`get_event()` will return some combination of a SQLAlchemy object representing a specific Event and the serialized (i.e. converted to dict) version of the Event.

Two patterns which all proxies should follow : 
- Serialization (which involves converting a SQLAlchemy model to a dict) happens at the EventProxy level, not at the business logic level.
- The function allows for choosing whether or not to return a serialized version of the event retrieved.  The reason for this is because this function could be called from other EventProxy functions and from business logic code.  We don't want to waste time serializing if another EventProxy function is calling `get_event()`.  But if it is being called by business logic code we always want to return a serialized version of the event found, because this serialized version is what will eventually make it to the user. 

Next let's look at the Event SQLAlchemy model...

## Event model
     
SQLalchemy models are classes that represent tables in a database and the relationships between those tables (i.e. one-to-one, one-to-many, many-to-many).  A single `Event` (i.e. papa 20) is represented by the `Events` model in `models/Events.py`
     
```
     def generate_event_model(db):
         class Events(db.Model):
           event_id = db.Column(db.Integer, primary_key=True)
           event_name = db.Column(db.String(80), unique=True, nullable=False)
                                 
           def __repr__(self):
             return '<Event %r>' % self.event_name
         return Events
```
                                                         
The name of the model class is the name used for the table in the database - this is why it is named `Events` instead of `Event` because we want the table to have the plural name.  The `Events` model has two fields - the `event_id` (which gets auto-generated by the database) and the `event_name` which is the name of the event (i.e. PAPA 20).  The `generate_event_model()` returns the generated `Events` class, and expects a `SQLalchemy` object (which will be the SQLAlchemy object that is created at startup) as an argument.  SQLAlchemy models are generated at runtime because it makes unit testing much easier.
                                                         
## Unit and Integration tests
Unit tests are located under `tests/unit` and integration tests are located under `tests/integration`.  The following command will run the unit tests : ``.  The following command will run the integration tests : ``.  Please review the unit tests and integration tests for the skeleton to get an understanding of what is expected from both types of tests.

## Next Steps

Congratulations!  You now have an understanding of the architecture of PSS_Qualifying.  There several things to do next after checking out the master branch
- look at the architectural reviews.  Any time there is a change to the architecture or a shared interface in PSS_Qualifying then that change should be recorded as a AR.
- review the unit and integration tests.  These will provide some insight into how the individual components of the pss_qualyfing work.
- look at the GitHub issues for this repo to see what tasks still need to be done

