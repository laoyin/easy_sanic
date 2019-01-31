#coding=utf-8
# from restful.operation_headler import Machine
# from sanic import request
from views.xauth import ProvilegeRole
def app_url(app):
    # app.router.add(uri='/token', methods=['GET'], handler=None)
    # app.router.add(uri='/user_login', methods=['POST'], handler=None)
    # app.router.add(uri='/user_register', methods=['POST'], handler=None)
    # app.router.add(uri='/service', methods=['POST'], handler=None)
    # app.router.add(uri='/role', methods=['POST'], handler=None)
    # app.router.add(uri='/service_api', methods=['POST'], handler=None)
    # app.router.add(uri='/service_permission', methods=['POST'], handler=None)
    app.router.add(uri='/machine', methods=['GET', 'POST'], handler=ProvilegeRole().as_views)
