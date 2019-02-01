#coding=utf-8
"""
@author:yinxingpan
@date 2019-1-30
"""
from collections import namedtuple

SQL_FIELD_TYPE = namedtuple("type", ("sql_name"))

INTERGER = SQL_FIELD_TYPE("integer")
BOOLEAN = SQL_FIELD_TYPE("boolean")
VARCHAR = SQL_FIELD_TYPE("varchar")
TEXT = SQL_FIELD_TYPE("text")


def update_field_value_template(fieldobject, field_key, field_value):
    if not isinstance(fieldobject, FieldObject):
        raise Exception("field object not implement from FieldObject")

    if fieldobject.sql_field_type == INTERGER.sql_name:
        return "{k}={v}".format(k=field_key, v=field_value)
    elif fieldobject.sql_field_type == BOOLEAN.sql_name:
        if field_value not in (True, False):
            raise Exception("boolean value error")
        else:
            field_value = "TRUE" if field_value else "FALSE"
        return "{k}={v}".format(k=field_key, v=field_value)
    elif fieldobject.sql_field_type == VARCHAR.sql_name:
        return "{k}='{v}'".format(k=field_key, v=field_value)
    elif fieldobject.sql_field_type == TEXT.sql_name:
        return "{k}='{v}'".format(k=field_key, v=field_value)
    else:
        raise Exception("field type error")


def insert_field_value_template(fieldobject, field_value):
    if not isinstance(fieldobject, FieldObject):
        raise Exception("field object not implement from FieldObject")

    if fieldobject.sql_field_type == INTERGER.sql_name:
        return "{v}".format(v=field_value)
    elif fieldobject.sql_field_type == BOOLEAN.sql_name:
        if field_value not in (True, False):
            raise Exception("boolean value error")
        else:
            field_value = "TRUE" if field_value else "FALSE"
        return "{v}".format(v=field_value)
    elif fieldobject.sql_field_type == VARCHAR.sql_name:
        return "'{v}'".format(v=field_value)
    elif fieldobject.sql_field_type == TEXT.sql_name:
        return "'{v}'".format(v=field_value)
    else:
        raise Exception("field type error")




class FieldObject(object):

    def __init__(self, field_name, type):
        self.__field_name = field_name
        self.__field_type = type
        if INTERGER.sql_name in self.__field_type:
            self.sql_field_type = INTERGER.sql_name
        elif BOOLEAN.sql_name in self.__field_type:
            self.sql_field_type = BOOLEAN.sql_name
        elif VARCHAR.sql_name in self.__field_type:
            self.sql_field_type = VARCHAR.sql_name
        elif TEXT.sql_name in self.__field_type:
            self.sql_field_type = TEXT.sql_name
        else:
            raise Exception("not support this field type")

    @property
    def field_name(self):
        return self.__field_name

    @property
    def field_message(self):
        return self.__field_type



class TableName(object):

    def __init__(self, name):
        self.__name = name

    @property
    def table_name(self):
        return self.__name


class SqlObject(type):

    def __new__(cls, name, bases, attrs):
        mappings = dict()
        for k, v in attrs.items():
            if isinstance(v, FieldObject):
                mappings[k] = v

        attrs['__mapping__'] = mappings
        if 'table_name' in attrs:
            attrs['__table__'] = attrs['table_name'].table_name
        return type.__new__(cls, name, bases, attrs)

    def generate_sql(self):
        raw_sql_list = []
        for k, v in self.__mapping__.items():
            raw_sql_list.append(
                "{field_name} {field_message}".format(field_name=v.field_name, field_message=v.field_message)
            )
        raw_field_sql = ' ,'.join(raw_sql_list)
        return "CREATE TABLE {table_name} ( {field_sql} )".format(table_name=self.__table__, field_sql=raw_field_sql)


    async def filter(self, request, **kwargs):

        field_list = []
        for k, v in self.__mapping__.items():
            field_list.append(
                "{field_name}".format(field_name=v.field_name)
            )
        sql_field_name = ",".join(field_list)

        condition_list = []
        for k, v in kwargs.items():
            if k not in self.__mapping__:
                raise Exception("field error")
            # condition_list.append("{k}='{v}'".format(k=k, v=v))
            condition_list.append(update_field_value_template(self.__mapping__[k], k, v))
        sql_conditon = " and ".join(condition_list)
        sql = "SELECT {field_name} FROM {table_name} WHERE {condition}".format(field_name=sql_field_name, table_name=self.__table__, condition=sql_conditon)
        print(sql)
        async with request.app.db.acquire(request) as cur:
            data = await cur.fetch(sql)
            return data

    async def delete(self, request, **kwargs):

        field_list = []
        for k, v in self.__mapping__.items():
            field_list.append(
                "{field_name}".format(field_name=v.field_name)
            )
        sql_field_name = ",".join(field_list)

        condition_list = []
        for k, v in kwargs.items():
            if k not in self.__mapping__:
                raise Exception("field error")
            # condition_list.append("{k}='{v}'".format(k=k, v=v))
            condition_list.append(update_field_value_template(self.__mapping__[k], k, v))
        if condition_list:
            sql_conditon = " and ".join(condition_list)
            sql = "DELETE FROM {table_name} WHERE {condition}".format(field_name=sql_field_name, table_name=self.__table__, condition=sql_conditon)
        else:
            sql = "DELETE FROM {table_name} ".format(table_name=self.__table__)
        print(sql)
        async with request.app.db.transaction(request) as cur:
            data = await cur.execute(sql)
            return data


    async def raw_sql(self, request, raw_sql):
        async with request.app.db.acquire(request) as cur:
            data = await cur.execute(raw_sql)
            return data


class BaseObject(metaclass=SqlObject):
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            if k not in self.__mapping__:
                raise Exception("error init,%s"%k)
            setattr(self, k, v)

    def __field_list(self):
        field_list = []
        primary_key = None
        for k, v in self.__mapping__.items():
            field_list.append(
                "{field_name}".format(field_name=v.field_name)
            )
            if 'primary key' in v.field_message:
                primary_key = v.field_name
        return field_list, primary_key



    async def save(self, request):

        if not isinstance(self, BaseObject):
            raise Exception("object error")
        field_list, primary_key = self.__field_list()

        condition_update = []
        values_list = []
        field_key = []
        for field in field_list:
            if isinstance(getattr(self, field), FieldObject):
                pass
            else:
                field_key.append(field)
                # values_list.append("'{key}'".format(key=getattr(self, field)))
                values_list.append(insert_field_value_template(self.__mapping__[field], getattr(self, field)))

            if field == primary_key or isinstance(getattr(self, field), FieldObject):
                continue
            else:
                # condition_update.append("{field_name}='{self_value}'".format(field_name=field, self_value=getattr(self, field)))
                condition_update.append(update_field_value_template(self.__mapping__[field], field, getattr(self, field)))

        sql_update = ','.join(condition_update)
        sql_values = ', '.join(values_list)
        sql_field = ','.join(field_key)

        insert_sql = "INSERT INTO {table_name} ({sql_field}) VALUES ({field_values}) ON CONFLICT ({primary_key}) DO UPDATE  SET {condition_update}".format(
            table_name=self.__table__, sql_field=sql_field, field_values=sql_values, condition_update=sql_update, primary_key=primary_key
        )
        print(insert_sql)
        async with request.app.db.transaction(request) as cur:
            data = await cur.execute(insert_sql)
            return data