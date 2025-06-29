import flet as ft


class HomeView(ft.View):
    def __init__(self, page: ft.Page):
        super().__init__()
        self.page = page
        self.route = '/'
        username = page.session.get('username')
        self.controls = [
            ft.AppBar(title=ft.Text(f"Jury System, user: {username}"), bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST),
            ft.ElevatedButton("Users", on_click=lambda _: self.page.go("/users")),
            ft.ElevatedButton("Settings", on_click=lambda _: self.page.go("/settings")),
        ]

    def did_mount(self):
        print('Did mount')
        self.update()

    def will_unmount(self):
        print('Will unmount')
