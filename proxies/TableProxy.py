from proxies.EventsProxy import EventsProxy

class PssDeserializers():
    def __init__(self,app,table_proxy):
        self.app = app
        self.table_proxy = table_proxy        
        
class TableProxy():
    def __init__(self, sqlAlchemyHandle, app):
        self.sqlAlchemyHandle = sqlAlchemyHandle        
        self.events_proxy = EventsProxy(self.sqlAlchemyHandle)
        
    def commit_changes(self):
        self.sqlAlchemyHandle.session.commit()
        
