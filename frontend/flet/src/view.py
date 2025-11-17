import os
import sys
import flet as ft
from redis import StrictRedis

sys.path.append(os.path.join(os.path.dirname(__file__), "../.."))
from shared.database import JuryDatabase

class View(ft.View):
    def __init__(self, page: ft.Page, autocommit=True):
        super().__init__()
        self.page = page
        self.db = JuryDatabase('db', autocommit)
        self.redis = StrictRedis(host='redis', port=6379, db=0, password='redispass', decode_responses=True)

    def did_mount(self):
        print(f'{type(self).__name__} did_mount')
        super().update()

    def will_unmount(self):
        print(f'{type(self).__name__} will_unmount')

    def host(self) -> str:
        return os.environ['DOMAIN']

    def token(self):
        return self.page.session.get('token')

    def setToken(self, token: str):
        self.page.session.set('token', token)
        self.redis.setex(token, 3600, 1)