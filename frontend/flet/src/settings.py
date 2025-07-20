import flet as ft
from view import View


class SiteView(View):
    def __init__(self, page: ft.Page):
        super().__init__(page)
        self.route = '/settings'
        self.controls = [
            ft.AppBar(title=ft.Text('Settings'), bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST),
            ft.ElevatedButton('Home', on_click=lambda _: self.page.go('/')),
        ]

