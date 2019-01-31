import ujson
import re
from itertools import repeat
from sanic.views import CompositionView
from views import api_dict

class APIClient(object):

    def __init__(self, app):
        self._app = app
        self._url_map = {}
        self.url_map = {}
        for uri, route in app.router.routes_all.items():
            self.url_map.update({
                uri: {
                    'method': route.methods,
                    'parameters': [p.name for p in route.parameters],
                    'rest_handler': api_dict.get(uri)
                }
            })