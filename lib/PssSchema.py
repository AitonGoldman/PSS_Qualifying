from marshmallow import fields as marshmallow_fields
from proxies import TableProxyError

class PssSchemaBuilder(object):    
    
    def __init__(self,app,model_name,model,exclude=None,session=None,test_marshmallow_fields=None):
        self.app = app                        
        self.model_name = model_name
        self.model = model
        self.exclude = exclude
        self.session = session
        self.marshmallow_fields = test_marshmallow_fields if test_marshmallow_fields else marshmallow_fields

    def initialize_pss_schema(self):
        self.schema = self.build_schema(self.model)
        return self
    
    def build_schema(self,model,depth=0):        
        relationships = {}                
        for relationship in model.__mapper__.relationships:                                     
            new_schema = self.build_schema(model=relationship.mapper.class_,depth=depth+1)            
            relationships[relationship.key]=self.marshmallow_fields.Nested(new_schema,many=relationship.uselist)            
        meta_params = {'model':model,'include_fk':True}
        if self.exclude:
            meta_params['exclude']=self.exclude
        if self.session:
            meta_params['sqla_session']=self.session
        meta_class = type("Meta",(object,),meta_params)
        schema_properties = {'Meta':meta_class}        
        for key,relationship in relationships.items():
            schema_properties[key]=relationship        
        schema = type(self.model_name+"Schema%s"%depth,(self.app.ma.ModelSchema,),schema_properties)        
        return schema
            
    def add_sqlAlchemy_relationship_to_schema(self,field_name,nested_schema,many=True):
        self.schema._declared_fields[field_name]=self.app.ma.Nested(nested_schema,many=many)

    def get_schema(self):
        return self.schema
    
    def deserialize(self, dict, instance=None):
        #TODO : it would make testing much easier if .data was returned here, but would need a way to check deserialize failure (maybe directly?)
        return self.schema().load(dict,instance=instance)

    def check_deserialize_failures(self, result):
        if len(list(result.errors.keys())) > 0:                        
            raise TableProxyError(str(result.errors))
