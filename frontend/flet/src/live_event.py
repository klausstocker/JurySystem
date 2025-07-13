import os
import sys
import flet as ft
from apscheduler.schedulers.background import BackgroundScheduler
import time

sys.path.append(os.path.join(os.path.dirname(__file__), "../.."))
from shared.database import JuryDatabase, User, Athlete, Attendance, Event, Progress, Rating

def header():
    return ['Name', 'Team', 'Category', 'Discipline', 'Difficulty', 'Execution', 'Sum']

def ratingAsRow(user: User, athlete: Athlete, attendance: Attendance, event: Event, rating: Rating):
    cells = [
        ft.DataCell(ft.Text(athlete.name())),
        ft.DataCell(ft.Text(user.team)),
        ft.DataCell(ft.Text(attendance.eventCategoryName)),
        ft.DataCell(ft.Text(rating.eventDisciplineName)),
        ft.DataCell(ft.Text(rating.difficulty)),
        ft.DataCell(ft.Text(rating.execution)),
        ft.DataCell(ft.Text(rating.sum()))
        ]
    return ft.DataRow(cells=cells)

class LiveEventView(ft.View):
    def __init__(self, page: ft.Page, eventId: int):
        super().__init__()
        self.page = page
        self.route =f'/public/liveEvent/{eventId}'

        def onServerTime():
            t = time.strftime('%H:%M:%S', time.localtime())
            self.controls = [
                ft.AppBar(title=ft.Text(f'Live ratings of {event.name}, {t}'), bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST),
                self.table
            ]
            self.page.update()

        self.scheduler = BackgroundScheduler()
        self.scheduler.add_job(onServerTime, 'interval', seconds=1)
        self.scheduler.start()
        
        db = JuryDatabase('db')
        event = db.getEvent(eventId)
        rows = []
        maxRows = 25 # todo this should be a setting
        for rating in db.getEventRatings(eventId, maxRows):
            athlete = db.getAthlete(rating.athleteId)
            user = db.getUser(athlete.userId)
            att = db.getAttendance(athlete.id, eventId)
            rows.append(ratingAsRow(user, athlete, att, event, rating))
        print(f'extracted {len(rows)} ratings')
        self.table = ft.DataTable(
                columns=[ft.DataColumn(ft.Text(h)) for h in header()],
                rows=rows
            )
        self.controls = [
            ft.AppBar(title=ft.Text(f'Live ratings of {event.name}'), bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST),
            self.table
        ]

