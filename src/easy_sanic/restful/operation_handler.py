#coding=utf-8
"""
@author yinxingpan
"""
from easy_sanic.utils.utils import generate_slat, RestStatus

class OperationsHandlerType(type):

    callmap = {
        "GET":"get",
        "POST":"post",
        "PUT":"put",
        "DELETE":"delete"
    }

    def __new__(cls, name, bases, attrs):
        mappings = dict()
        for k, v in attrs.items():
            if k.upper() in OperationsHandlerType.callmap:
                mappings[k.upper()] = v

        exports = {}
        for key, value in attrs.items():
            export = getattr(value, "export", None)
            if export is not None:
                exports[export] = value


        attrs['__export__'] = exports
        attrs['__mapping__'] = mappings
        return type.__new__(cls, name, bases, attrs)




class ResourceBase(metaclass=OperationsHandlerType):

    def as_views(self, request, *args, **kwargs):
        request['span'] = None
        if request.method in ResourceBase.callmap:

            if request.method in ["GET", "POST"]:
                if "operation" in request.args:
                    func = self.__export__.get((request.method, request.args['operation'][0]))
                    if func:
                        return func(self, request=request)
                    else:
                        return RestStatus.response_status(404, "request method error")
                else:
                    func = self.__mapping__.get(request.method)
                    if func:
                        return func(self, request=request)
                    else:
                        return RestStatus.response_status(404, "request method error")
            else:
                func = self.__mapping__.get(request.method)
                if func:
                    return func(self, request=request)
                else:
                    return RestStatus.response_status(404, "request method error")

        else:
            return RestStatus.response_status(400, "request method error")



def operation(flag):
    method = "GET" if flag else "POST"

    def _decorator(func):
        func.export = method, func.__name__
        return func
    return _decorator