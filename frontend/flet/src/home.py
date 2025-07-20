import os
import sys
import flet as ft
from view import View

sys.path.append(os.path.join(os.path.dirname(__file__), "../.."))
from shared.database import JuryDatabase, Athlete, Gender
class HomeView(View):
    def __init__(self, page: ft.Page):
        super().__init__(page)
        self.route = '/'
        user = page.session.get('user')
        username = '' if user is None else user.username
        self.controls = [
            ft.AppBar(title=ft.Text(f"Jury System, user: {username}"), bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST),
            ft.ElevatedButton("Users", on_click=lambda _: self.page.go("/users")),
            ft.ElevatedButton("Athletes", on_click=lambda _: self.page.go("/athletes")),
            ft.ElevatedButton("Settings", on_click=lambda _: self.page.go("/settings")),
            ft.ElevatedButton("Logout", on_click=self.logout),
        ]

    def logout(self, e):
        self.page.session.clear()
        self.page.go('/login')


class LoginView(View):
    def __init__(self, page: ft.Page):
        super().__init__(page)
        self.route = '/login'

        def loginbtn(e):
            userId = self.db.validateUser(username.value, password.value)
            if userId is not None:
                print("Redirecting...")
                self.page.session.set('user', self.db.getUser(userId))
                if self.page.session.contains_key('target'):
                    target = self.page.session.get('target')
                    self.page.session.remove('target')
                    self.page.route = target
                    self.page.on_route_change(ft.RouteChangeEvent(target))
                else:
                    self.page.go('/')
            else:
                print("Login failed !!!")
                self.page.open(ft.SnackBar(
                    ft.Text("wrong login, user expired or locked", size=30),
                    bgcolor="red"
                ))

        username = ft.TextField(label="User name")
        password = ft.TextField(label="Password", password=True, can_reveal_password=True, on_submit=loginbtn)
    
        self.controls = [username, password,ft.ElevatedButton("Login Now",
                                  bgcolor="blue", color="white",
                                  on_click=loginbtn)]



