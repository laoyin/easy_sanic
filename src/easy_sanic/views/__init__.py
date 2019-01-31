#coding=utf-8
from views.user_views import UserLogin, UserRegister, LoginMessage
from views.auth_filter import TokenFilter
from views.xauth import ProvilegeRole


api_dict = {
    '/login_message': LoginMessage(),
    '/token': TokenFilter(),
    '/user_login': UserLogin(),
    '/user_register': UserRegister(),
    '/test': LoginMessage(),
    '/role':ProvilegeRole()
}