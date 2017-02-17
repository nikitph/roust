from eve import Eve
from eve_mongoengine import EveMongoengine
from eve.auth import BasicAuth

# init application
from public.models import *
from user.models import User

MONGODB_SETTINGS = {

    # 'MONGO_HOST': 'localhost',
    #     'MONGO_PORT': 27017,
    #     'MONGO_USERNAME' : None,
    # 'MONGO_PASSWORD': None,
    'MONGO_DBNAME': 'houzee',
    'X_DOMAINS': '*',
    'ALLOW_OVERRIDE_HTTP_METHOD': 'true',
    'query_objectid_as_string': 'True',
    'JSON_SORT_KEYS': 'true',
    'DOMAIN': {'resident': {}},
    'PAGINATION_LIMIT': 200,
    'max_results': 80
}


class MyBasicAuth(BasicAuth):
    def check_auth(self, username, password, allowed_roles, resource,
                   method):
        return username == 'admin' and password == 'secret'


app = Eve(settings=MONGODB_SETTINGS, auth=MyBasicAuth)
# init extension
ext = EveMongoengine(app)
# register model to eve
ext.add_model(Resident)
ext.add_model(Township)
ext.add_model(Item, query_objectid_as_string='true')
ext.add_model(Message, query_objectid_as_string='true')

# let's roll
app.run(host='127.0.0.1', port=8001, debug=True)
