from flask_principal import Permission
from lib.auth import needs

class EventCreatorPermission(Permission):
    def __init__(self):
        event_create_need = needs.EventCreatorRoleNeed()
        super(EventCreatorPermission, self).__init__(event_create_need)

class EventEditPermission(Permission):
    def __init__(self,event_id):        
        edit_need = needs.EventEditNeed(event_id)
        super(EventEditPermission, self).__init__(edit_need)
        
                 
