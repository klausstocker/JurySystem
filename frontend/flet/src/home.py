import flet as ft


class HomeView(ft.View):
    def __init__(self, page: ft.Page):
        super().__init__()
        self.page = page
        self.route = '/'
        self.controls = [
            ft.AppBar(title=ft.Text("Flet app"), bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST),
            ft.ElevatedButton("Go to settings", on_click=lambda _: self.page.go("/settings")),
        ]

    def did_mount(self):
        print('Did mount')
        self.update()

    def will_unmount(self):
        print('Will unmount')
