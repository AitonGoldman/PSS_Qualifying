import random
from flask import Flask
from app import create_app
from lib.DbHelper import DbHelper,POSTGRES_TYPE
from decouple import config
import os,sys

test_db_name_for_run='test_db_%s' % random.randrange(9999999)
app=None

def static_setup():    
    global app,test_db_name_for_run,PSS_ADMIN_EVENT,pss_config    
    if app is None:
        app = create_app({'pss_db_name':test_db_name_for_run})         
        app.db_helper.create_db_and_tables(app)
    return app
