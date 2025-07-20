import os
import sys
import flet as ft

sys.path.append(os.path.join(os.path.dirname(__file__), "../.."))
from shared.database import JuryDatabase

class View(ft.View):
    def __init__(self, page: ft.Page):
        super().__init__()
        self.page = page
        self.db = JuryDatabase('db')

    def did_mount(self):
        print(f'{type(self).__name__} did_mount')
        super().update()

    def will_unmount(self):
        print(f'{type(self).__name__} will_unmount')