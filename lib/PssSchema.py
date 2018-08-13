class PssSchemaBuilder(object):    
    
    def __init__(self,app,model_name,model,exclude=None,session=None):
        self.app = app                        
        self.model_name = model_name
        self.model = model
        self.exclude = exclude
        self.session = session
        self.build_schema()
        
    def build_schema(self):        
        meta_params = {'model':self.model,'include_fk':True}
        if self.exclude:
            meta_params['exclude']=self.exclude
        if self.session:
            meta_params['sqla_session']=self.session
        meta_class = type("Meta",(object,),meta_params)
        self.schema = type(self.model_name+"Schema",(self.app.ma.ModelSchema,),{'Meta':meta_class})        
        
    def add_sqlAlchemy_relationship_to_schema(self,field_name,nested_schema,many=True):
        self.schema._declared_fields[field_name]=self.app.ma.Nested(nested_schema,many=many)

    def get_schema(self):
        return self.schema
    
    def get_serializer(self):
        return self.schema()
