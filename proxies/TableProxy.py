from proxies.EventsProxy import EventsProxy
        
class TableProxy():
    def __init__(self, sqlAlchemyHandle, app):
        self.sqlAlchemyHandle = sqlAlchemyHandle        
        self.events_proxy = EventsProxy(self.sqlAlchemyHandle)
        
    def commit_changes(self):
        self.sqlAlchemyHandle.session.commit()
        
