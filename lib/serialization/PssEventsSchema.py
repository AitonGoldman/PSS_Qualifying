def gen_events_schema(app,table_proxy) :     
    class EventsSchema(app.ma.ModelSchema):
        class Meta:
            model = table_proxy.events_proxy.event_model
    return EventsSchema
