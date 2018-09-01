import unittest
from mock import MagicMock
from pss_unit_test_base import PssUnitTestBase
from lib.PssSchema import PssSchemaBuilder
from marshmallow_sqlalchemy import ModelSchema
from marshmallow import fields as marshmallow_fields

class PssSchemaLibTest(PssUnitTestBase):
    def setUp(self):
        pass
    def initialize_mock_nested_relationship(self):
        mock_relationship = MagicMock()
        mock_relationship.key="mock_relationship"
        mock_relationship.uselist=False        
        mock_relationship.mapper.class_.__mapper__=MagicMock()        
        return mock_relationship
    
    def test_pss_schema(self):                        
        mock_app = MagicMock()
        mock_app.ma.ModelSchema = ModelSchema
        model_name = "test_model"
        mock_model = MagicMock()
        mock_model.__mapper__=MagicMock()
        mock_session = MagicMock()
        mock_marshmallow_fields = MagicMock()
        mock_marshmallow_fields.Nested = marshmallow_fields.Nested        
        mock_relationship = self.initialize_mock_nested_relationship()
        mock_model.__mapper__.relationships=[mock_relationship]
        
        
        pss_schema_builder = PssSchemaBuilder(mock_app,
                                              model_name,
                                              mock_model,
                                              session=mock_session,
                                              test_marshmallow_fields=mock_marshmallow_fields)

        test_schema = pss_schema_builder.initialize_pss_schema()        
        self.assertEqual(test_schema.schema.__name__,"test_modelSchema0")                
        self.assertEqual(type(test_schema.schema._declared_fields.get('mock_relationship',None)),marshmallow_fields.Nested)
                
