import flet as ft
import re
from home import HomeView
from settings import SiteView
from users import UserView, UserEditView
from athletes import AthleteView


class RouteErrorView(ft.View):
    def __init__(self):
        super().__init__()
        self.controls = [ft.Text('Access Denied')]

    def did_mount(self):
        self.page.update()


class Navigator:
    def __init__(self, page: ft.Page):
        self.page = page

    def route_change(self, route):
        print(f'{route=}')
        self.page.views.clear()
        self.page.views.append(HomeView(self.page))
        if self.page.route == '/settings':
            self.page.views.append(SiteView(self.page))
        if self.page.route == '/users':
            self.page.views.append(UserView(self.page))
        if self.page.route.startswith('/userEdit'):
            userId = int(self.page.route.split('/')[-1])
            self.page.views.append(UserEditView(self.page, userId))
        if self.page.route == '/athletes':
            self.page.views.append(AthleteView(self.page))
        self.page.update()

    def view_pop(self, view):
        self.page.views.pop()
        try:
            top_view = self.page.views[-1]
            self.page.go(top_view.route)
        except IndexError:
            self.page.views.append(HomeView(self.page))
