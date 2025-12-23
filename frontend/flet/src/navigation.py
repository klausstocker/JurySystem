import flet as ft
import secrets
import sys
import os
from home import HomeView, LoginView
from settings import SiteView
from users import UserView, UserEditView
from athletes import AthleteView, AthleteEditView
from attendance import AttendanceView
from events import EventView, EventEditView
from rating import RatingView
from ranking import RankingView
from live_event import LiveEventView
from categories import CategoriesView

sys.path.append(os.path.join(os.path.dirname(__file__), "../.."))
from shared.database import JuryDatabase, Event, Progress

class RouteErrorView(ft.View):
    def __init__(self):
        super().__init__()
        self.controls = [ft.Text('Access Denied')]

    def did_mount(self):
        self.page.update()


class Navigator:
    def __init__(self, page: ft.Page, db, redis):
        self.page = page
        self.db = db
        self.redis = redis

    def token(self):
        return self.page.session.get('token')

    def setToken(self, token: str):
        self.page.session.set('token', token)
        self.redis.setex(token, 3600, 1)

    def route_change(self, route):
        print(f'{route=}')
        self.page.views.clear()
        self.page.views.append(HomeView(self.page, self.db, self.redis))
        if self.page.route.startswith('/public/liveEvent'):
            eventId = int(self.page.route.split('/')[-1])
            print(f'switch to live event {eventId}')
            self.page.views.append(LiveEventView(self.page, eventId, self.db, self.redis ))
            self.page.update()
            return
        elif self.page.route.startswith('/public/ranking'):
            eventId = int(self.page.route.split('/')[-1])
            print(f'switch to public ranking {eventId}')
            self.page.views.append(RankingView(self.page, eventId, self.db, self.redis))
            self.page.update()
            return
        elif self.page.route.startswith("/categories"):
            eventId = int(self.page.route.split("/")[-1])
            self.page.views.append(CategoriesView(self.page, eventId, self.db, self.redis))
            self.page.update()
            return
        elif self.page.route == '/login':
            self.page.views.append(LoginView(self.page, self.db, self.redis))
        elif self.page.route.startswith('/autoLogin'):
            user = self.page.route.split('/')[2]
            token = self.page.route.split('/')[3]
            userId = self.db.validateUserByToken(user, token)
            if userId is not None:
                print(f"Redirecting user '{user}' logged in with url")
                self.page.session.set('user', self.db.getUser(userId))
                self.setToken(secrets.token_urlsafe())
                self.page.go('/')
            else:
                self.page.go('/login')
        elif self.page.session.get('user') is None:
            print(f'store target={self.page.route}')
            self.page.session.set('target', self.page.route)
            self.page.views.append(LoginView(self.page, self.db, self.redis))
        elif self.page.route == '/settings':
            self.page.views.append(SiteView(self.page, self.db, self.redis))
        elif self.page.route == '/users':
            self.page.views.append(UserView(self.page, self.db, self.redis))
        elif self.page.route.startswith('/userEdit'):
            userId = int(self.page.route.split('/')[-1])
            self.page.views.append(UserEditView(self.page, self.db, self.redis, userId))
        elif self.page.route == '/athletes':
            self.page.views.append(AthleteView(self.page, self.db, self.redis))
        elif self.page.route.startswith('/athleteEdit'):
            athleteId = int(self.page.route.split('/')[-1])
            self.page.views.append(AthleteEditView(self.page, self.db, self.redis, athleteId))
        elif self.page.route.startswith('/attendances'):
            self.page.views.append(AttendanceView(self.page, self.db, self.redis))
        elif self.page.route == '/events':
            self.page.views.append(EventView(self.page, self.db, self.redis))
        elif self.page.route.startswith('/eventEdit'):
            eventId = int(self.page.route.split('/')[-1])
            self.page.views.append(EventEditView(self.page, self.db, self.redis, eventId))
        elif self.page.route.startswith('/rating'):
            eventId = int(self.page.route.split('/')[-1])
            self.page.views.append(RatingView(self.page, self.db, self.redis, eventId))
        else:
            self.page.views.append(HomeView(self.page, self.db, self.redis))
        self.page.update()

    def view_pop(self, view):
        self.page.views.pop()
        try:
            top_view = self.page.views[-1]
            self.page.go(top_view.route)
        except IndexError:
            self.page.views.append(HomeView(self.page, self.db, self.redis))
