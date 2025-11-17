import flet as ft
from home import HomeView, LoginView
from settings import SiteView
from users import UserView, UserEditView
from athletes import AthleteView, AthleteEditView
from attendance import AttendanceView
from events import EventView, EventEditView
from rating import RatingView
from ranking import RankingView
from live_event import LiveEventView


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
        if self.page.route.startswith('/public/liveEvent'):
            eventId = int(self.page.route.split('/')[-1])
            print(f'switch to live event {eventId}')
            self.page.views.append(LiveEventView(self.page, eventId))
            self.page.update()
            return
        elif self.page.route.startswith('/public/ranking'):
            eventId = int(self.page.route.split('/')[-1])
            print(f'switch to public ranking {eventId}')
            self.page.views.append(RankingView(self.page, eventId))
            self.page.update()
            return
        elif self.page.route == '/login':
            self.page.views.append(LoginView(self.page))
        elif self.page.session.get('user') is None:
            print(f'store target={self.page.route}')
            self.page.session.set('target', self.page.route)
            self.page.views.append(LoginView(self.page))
        elif self.page.route == '/settings':
            self.page.views.append(SiteView(self.page))
        elif self.page.route == '/users':
            self.page.views.append(UserView(self.page))
        elif self.page.route.startswith('/userEdit'):
            userId = int(self.page.route.split('/')[-1])
            self.page.views.append(UserEditView(self.page, userId))
        elif self.page.route == '/athletes':
            self.page.views.append(AthleteView(self.page))
        elif self.page.route.startswith('/athleteEdit'):
            athleteId = int(self.page.route.split('/')[-1])
            self.page.views.append(AthleteEditView(self.page, athleteId))
        elif self.page.route.startswith('/attendances'):
            self.page.views.append(AttendanceView(self.page))
        elif self.page.route == '/events':
            self.page.views.append(EventView(self.page))
        elif self.page.route.startswith('/eventEdit'):
            eventId = int(self.page.route.split('/')[-1])
            self.page.views.append(EventEditView(self.page, eventId))
        elif self.page.route.startswith('/rating'):
            eventId = int(self.page.route.split('/')[-1])
            self.page.views.append(RatingView(self.page, eventId))
        self.page.update()

    def view_pop(self, view):
        self.page.views.pop()
        try:
            top_view = self.page.views[-1]
            self.page.go(top_view.route)
        except IndexError:
            self.page.views.append(HomeView(self.page))
