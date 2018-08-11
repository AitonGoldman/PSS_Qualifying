def gen_events_schema(app,table_proxy,pss_model=None) :     
    class EventsSchema(app.ma.ModelSchema):
        class Meta:
            model = table_proxy.events_proxy.event_model if pss_model is None else pss_model
    return EventsSchema()
