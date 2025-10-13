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

        menu = ft.Row(
            controls=[
                ft.TextButton("Users", on_click=lambda _: self.page.go("/users"),width= 120, height = 40,),
                ft.TextButton("Athletes", on_click=lambda _: self.page.go("/athletes"),width= 120, height = 40,style=ft.ButtonStyle(text_style=ft.TextStyle(size=16))),
                ft.TextButton("Events", on_click=lambda _: self.page.go("/events"),width= 120, height = 40,style=ft.ButtonStyle(text_style=ft.TextStyle(size=16))),
                ft.TextButton("Rating", on_click=lambda _: self.page.go("/rating/1"),width= 120, height = 40,style=ft.ButtonStyle(text_style=ft.TextStyle(size=16))),
                ft.TextButton("Settings", on_click=lambda _: self.page.go("/settings"),width= 120, height = 40,style=ft.ButtonStyle(text_style=ft.TextStyle(size=16))),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=40  
        )
        logout_button = ft.Row(
            controls=[
                ft.ElevatedButton(
                    "Logout",
                    on_click=self.logout,
                    color="black", 
                    width= 100,
                    height= 40,
                    style=ft.ButtonStyle(
                        bgcolor = {
                            ft.ControlState.DEFAULT: "lightblue",
                            ft.ControlState.HOVERED: "#42DDF5FF",
                        },
                        text_style=ft.TextStyle(size=16),
                    )    
                ),
            ],
        )


        self.controls = [
            ft.AppBar(
                title=ft.Row(
                    [
                        ft.Text("Jury System", size=18, weight="bold"),
                        ft.Container(expand=True),
                        menu,
                        ft.Container(expand=True),
                        ft.Text(f"user: {username}", size=14, italic=True),
                        logout_button,
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST,
            ),
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

        title = ft.Text("Anmeldung zum Jurysystem",size = 40, weight="bold")
        username = ft.TextField(label="User name", width=400, border_color= "white")
        password = ft.TextField(label="Password", password=True, border_color= "white", can_reveal_password=True, on_submit=loginbtn, width=400)
        login_button = ft.ElevatedButton(
            "Login Now",
            bgcolor="blue",
            color="white",
            on_click=loginbtn
        )

        
        self.controls = [
            ft.Container(
                content=ft.Column(
                    [
                        title,
                        username,
                        password,
                        login_button
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=20
                ),
                expand=True,
                alignment=ft.alignment.center
            )
        ]
