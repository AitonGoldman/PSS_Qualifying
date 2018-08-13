import unittest
from mock import MagicMock
from pss_unit_test_base import PssUnitTestBase
from lib.PssSchema import PssSchemaBuilder

class SerializersTest(PssUnitTestBase):
    def setUp(self):
        pass
    
    def test_smoke_test_pss_schema_builder(self):                                                
        fake_session=MagicMock()        
        test_schema = PssSchemaBuilder(self.fake_app,"Test",self.fake_model_parent,session=fake_session).get_schema()
        self.assertTrue(test_schema.Meta is not None)
        self.assertEqual(test_schema.Meta.model,self.fake_model_parent)        

    def test_exclude_fields_from_schema(self):                                                
        fake_session=MagicMock()
        excluded_fields = ['test_association']
        test_schema = PssSchemaBuilder(self.fake_app,"Test",self.fake_model_parent,session=fake_session,exclude=excluded_fields).get_schema()
        self.assertTrue(test_schema.Meta is not None)
        self.assertEqual(test_schema.Meta.model,self.fake_model_parent)
        self.assertEqual(test_schema.Meta.exclude,excluded_fields)
        
    def test_add_relationship_to_schema(self):                                                
        fake_session=MagicMock()        
        child_schema = PssSchemaBuilder(self.fake_app,"FakeModelParent",self.fake_model_parent,session=fake_session).get_schema()
        parent_schema_builder = PssSchemaBuilder(self.fake_app,"FakeModelParent",self.fake_model_parent,session=fake_session)
        parent_schema_builder.add_sqlAlchemy_relationship_to_schema('test_association',child_schema)
        parent_schema = parent_schema_builder.get_schema()
        self.assertIn('test_association', parent_schema._declared_fields)
        self.assertTrue(parent_schema.Meta is not None)
        self.assertEqual(parent_schema.Meta.model,self.fake_model_parent)

    def test_get_serializer(self):
        fake_session=MagicMock()                
        fake_model_child_instance = self.fake_model_child()
        fake_session.query().get.return_value=fake_model_child_instance
        test_serializer = PssSchemaBuilder(self.fake_app,"Test",self.fake_model_parent,session=fake_session).get_serializer()        
        deserialized_object = test_serializer.load({}).data        
        self.assertIsInstance(deserialized_object,self.fake_model_parent)
        
