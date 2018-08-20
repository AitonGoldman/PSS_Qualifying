from flask import Flask
from lib.DbHelper import DbHelper,POSTGRES_TYPE
from decouple import config
import os,sys

if len(sys.argv) > 1:
    pss_db_name=sys.argv[1]    
else:
    print("didn't specify db name...")
    sys.exit(1)

real_app = Flask('dummy')

pss_db_type = config('pss_db_type',default='postgres')
pss_db_username = config('db_username')
pss_db_password = config('db_password')

db_helper = DbHelper(pss_db_type,pss_db_username,pss_db_password,pss_db_name)
db_helper.create_db_and_tables(real_app)

# pss_config.get_db_info().create_db_and_tables(real_app,True)
# db_handle = pss_config.get_db_info().create_db_handle(real_app)
# table_proxy=TableProxy()
# table_proxy.initialize_tables(db_handle)
# #bootstrap.bootstrap_pss_admin_event(tables,'pss_admin')
# #bootstrap.bootstrap_roles(tables)
# table_proxy.create_role(roles_constants.TOURNAMENT_DIRECTOR)
# table_proxy.create_role(roles_constants.SCOREKEEPER)
# table_proxy.create_role(roles_constants.DESKWORKER)

# table_proxy.create_user('test_user_admin',
#                         'test_first_name',
#                         'test_last_name',
#                         admin_password,
#                         event_creator=True,
#                         commit=True)

# pss_config.get_db_info().load_machines_from_json(real_app,test=False,table_proxy=table_proxy)

