gunicorn app:app --bind 0.0.0.0:7001 --worker-class sanic.worker.GunicornWorker -w 2

easy sanic 框架，集成了sanic，同时自定义async orm， （目前支持postgres）
easyrestful。简单好用，你可以完全不用掌握python3 aysncio相关知识 也能写出高性能服务。

easy sanic 目标是 快速打造微服务。

easy sanic framework.

如何定义url：

url:
```python
from views.xauth import ProvilegeRole   
def app_url(app):
    app.router.add(uri='/token', methods=['GET'], handler=ProvilegeRole().as_views)

```


如何定义orm models：
orm:
models.py
```python
from db.orm import SqlObject, FieldObject, TableName

#User message
class User(metaclass=SqlObject):
    id = FieldObject('id', 'varchar(200) primary key')
    name = FieldObject('name', 'varchar(200)')
    password = FieldObject('password', 'varchar(200)')
    table_name = TableName('users')

```

如何定义views， 同时views 支持get、post、delete、put方法，并支持自定义扩展。
自定义扩展只限定在get、post请求。

使用装饰器 operation进行装饰，flag = True 表示get方法，False代表post方法。


比如 请求 get  http://127.0.0.1:/token/ 不能满足您的需求，您需要自定义其他方法

```python
    @operation(flag=True)
    def print_hh(self, request):
        print("i am print hh")

        return RestStatus.response_status(400, "request method error")

```
那么您即可通过 http://127.0.0.1:/token/?operation=print_hh 获取资源。



views:
xauth.py
```python
from db.dao import User
from restful.operation_headler import ResourceBase, operation


class ProvilegeRole(ResourceBase):

    async def get(self, request):
        data = await User.filter(request, id='yinxingpan')
        new_obj = User(id="yinxingpan", name="haha2", password="123")
        result = await new_obj.save(request)
        print(data)
        return RestStatus.response_status(200, "ok", data=data)

    async def post(self, request):
        request_data = request.form
        return RestStatus.response_status(200, "ok", data=data)

    def delete(self, request):
        print("i am delete")

        return RestStatus.response_status(400, "request method error")

    @operation(flag=True)
    def print_hh(self, request):
        print("i am print hh")

        return RestStatus.response_status(400, "request method error")
```
    
    
how to create all table
init_sql_table.py



