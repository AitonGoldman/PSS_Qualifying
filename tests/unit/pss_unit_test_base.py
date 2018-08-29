import unittest
from mock import MagicMock
from models.Events import generate_event_model

from flask_sqlalchemy import SQLAlchemy
from flask import Flask

class PssUnitTestBase(unittest.TestCase):    
    def __init__(self,*args, **kwargs):
        super(PssUnitTestBase, self).__init__(*args, **kwargs)                                
        #FIXME : need constants for these strings                        
        self.fake_app = Flask('poop')
        self.fake_app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False        
        self.db_handle = SQLAlchemy()
