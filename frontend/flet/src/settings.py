import flet as ft


class SiteView(ft.View):
    def __init__(self, page: ft.Page):
        super().__init__()
        self.page = page
        self.route = '/settings'
        self.controls = [
            ft.AppBar(title=ft.Text("Settings"), bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST),
            ft.ElevatedButton("Go Home", on_click=lambda _: self.page.go("/")),
        ]

    def did_mount(self):
        print('Did mount')
        self.update()

    def will_unmount(self):
        print('Will unmount')
