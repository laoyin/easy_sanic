#coding=utf-8
from easy_sanic.db.orm import SqlObject, FieldObject, TableName, BaseObject

#User message
class User(BaseObject):
    id = FieldObject('id', 'varchar(200) primary key')
    name = FieldObject('name', 'varchar(200)')
    password = FieldObject('password', 'varchar(200)')
    table_name = TableName('user_yin')

class ProvilegeRole(BaseObject):
    name = FieldObject("name", "varchar(200)")
    table_name = TableName('privilege_role')


class PrivilegeService(BaseObject):
    name = FieldObject("name", "varchar(200)")
    table_name = TableName('privilege_service')


class PrivilegeAPI(BaseObject):

    id = FieldObject('id', 'varchar(200) primary key')
    path = FieldObject('name', 'varchar(200)')
    service_id = FieldObject('password', 'varchar(200)')
    is_public = FieldObject('is_public', 'boolean')
    description = FieldObject('description', 'text')
    table_name = TableName('privilege_api')


class PrivilegePermission(BaseObject):
    role_id = FieldObject('role_id', 'varchar(256)')
    role_name = FieldObject('role_name', 'varchar(256)')
    service_id = FieldObject('service_id', 'varchar(256)')
    api_id = FieldObject('api_id', 'varchar(256)')
    table_name = TableName('privilege_permission')


__all__ = [
    User, ProvilegeRole, PrivilegeService, PrivilegeAPI, PrivilegePermission
]