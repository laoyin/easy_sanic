#coding=utf-8
from db.dao import User, ProvilegeRole, PrivilegeService, PrivilegeAPI, PrivilegePermission


async def init_tables(app):
    user_sql = User.generate_sql()
    role_sql = ProvilegeRole.generate_sql()
    service_sql = PrivilegeService.generate_sql()
    api_sql = PrivilegeAPI.generate_sql()
    async with app.db.transaction() as cur:
            data = await cur.execute(user_sql)

    async with app.db.transaction() as cur:
            data = await cur.execute(role_sql)

    async with app.db.transaction() as cur:
            data = await cur.execute(service_sql)

    async with app.db.transaction() as cur:
            data = await cur.execute(api_sql)

