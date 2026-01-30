import os
import sys
import flet as ft
import secrets
from view import View

sys.path.append(os.path.join(os.path.dirname(__file__), "../.."))
from shared.database import JuryDatabase, Athlete, Gender, Event, Progress, Restrictions
from shared.rights import Route, allowedRoutes

class TextButton(ft.TextButton):
    def __init__(self, text = None, icon = None, icon_color = None, content = None, style=ft.ButtonStyle(text_style=ft.TextStyle(size=16), side=ft.BorderSide(1, ft.Colors.OUTLINE)), autofocus = None, url = None, url_target = None, clip_behavior = None, on_click = None, on_long_press = None, on_hover = None, on_focus = None, on_blur = None, ref = None, key = None, width= 144, height = 48, left = None, top = None, right = None, bottom = None, expand = None, expand_loose = None, col = None, opacity = None, rotate = None, scale = None, offset = None, aspect_ratio = None, animate_opacity = None, animate_size = None, animate_position = None, animate_rotation = None, animate_scale = None, animate_offset = None, on_animation_end = None, tooltip = None, badge = None, visible = None, disabled = None, data = None, adaptive = None):
        super().__init__(text, icon, icon_color, content, style, autofocus, url, url_target, clip_behavior, on_click, on_long_press, on_hover, on_focus, on_blur, ref, key, width, height, left, top, right, bottom, expand, expand_loose, col, opacity, rotate, scale, offset, aspect_ratio, animate_opacity, animate_size, animate_position, animate_rotation, animate_scale, animate_offset, on_animation_end, tooltip, badge, visible, disabled, data, adaptive)

class HomeView(View):
    def __init__(self, page: ft.Page, db, redis):
        super().__init__(page, db, redis)
        self.route = '/'
        user = page.session.get('user')
        username = '' if user is None else user.username
        controls = []
        help_button = ft.Container(width=0)
        for allowed in allowedRoutes(user):
            route = allowed.route
            name = allowed.name
            if route == '/settings':
                help_button = ft.IconButton(icon=ft.Icons.HELP_OUTLINE, tooltip="Help", on_click=lambda _: self.page.go('/help'))
                continue
            if user and user.restrictions == Restrictions.TRAINER and route == '/events':
                continue
            if route.startswith('/rating'):
                route = '/rating'
            if allowed.name == 'Ranking':
                route = '/ranking_home'
            controls.append(TextButton(allowed.name, on_click=lambda _,r=route: self.page.go(r)))

        menu = ft.Column(
            controls=controls,
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=5
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
                            ft.ControlState.HOVERED: "#FFFFFFFF",
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
                        help_button,
                        ft.Text("Jury System", size=18, weight="bold"),
                        ft.Container(expand=True),
                        ft.Text(f"user: {username}", size=14, italic=True),
                        logout_button,
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST,
            ),
            ft.Container(
                content=menu,
                expand=True,
                alignment=ft.alignment.center
            )
        ]

    def logout(self, e):
        self.page.session.clear()
        self.page.go('/login')


class LoginView(View):
    def __init__(self, page: ft.Page, db, redis):
        super().__init__(page, db, redis)
        self.route = '/login'

        def loginbtn(e):
            userId = self.db.validateUser(userEdit.value, passEdit.value)
            if userId is not None:
                print("Redirecting...")
                self.page.session.set('user', self.db.getUser(userId))
                self.setToken(secrets.token_urlsafe())
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

        userEdit = ft.TextField(label="User name", width=400, border_color= "white")
        passEdit = ft.TextField(label="Password", password=True, border_color= "white", can_reveal_password=True, on_submit=loginbtn, width=400)
        login_button = ft.ElevatedButton(
            "Login",
            on_click=loginbtn,
            color="black", 
            width= 80,
            height= 30,

            style=ft.ButtonStyle(
                bgcolor = {
                    ft.ControlState.DEFAULT: "lightblue",
                    ft.ControlState.HOVERED: "#FFFFFFFF",
                },
                text_style=ft.TextStyle(size=16),
            )
        )

        controls = [
            ft.Text("Anmeldung zum Jurysystem",size = 40, weight="bold"),
            userEdit, passEdit,login_button
        ]

        print(len(self.db.getAllEvents()))
        for e in self.db.getAllEvents():
            if e.progress() == Progress.FINISHED:
                controls.append(ft.ElevatedButton(f"{e.descr()}", on_click=lambda _,id=e.id: self.page.go(f"/public/ranking/{id}")))
            if e.progress() == Progress.ACTIVE:
                controls.append(ft.ElevatedButton(f"{e.descr()}", on_click=lambda _,id=e.id: self.page.go(f"/public/liveEvent/{id}")))

        self.controls = [
            ft.Container(
                content=ft.Column(
                    controls=controls,
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=15
                ),
                expand=True,
                alignment=ft.alignment.center
            )
        ]