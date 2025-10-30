import os
import sys
import flet as ft
from view import View

sys.path.append(os.path.join(os.path.dirname(__file__), "../.."))
from shared.database import JuryDatabase, User, Athlete, Attendance, Gender, Event, Progress, Restrictions


def header():
    return ['', 'given name', 'surname', 'birth', 'gender', 'category', 'group']

class AttendanceView(View):
    def __init__(self, page: ft.Page):
        super().__init__(page)
        self.route = '/attendances'

        user = self.page.session.get('user')
        isHost = user.restrictions == Restrictions.HOST
        
        def printPdf(e):
            if self.eventCtrl.value is None:
                return
            eventId = self.eventCtrl.value
            host = self.page.url[5:]
            page.launch_url(f'https://api.{host}/attendances/{eventId}/{user.id}')

        def createRows():
            if self.eventCtrl.value is None:
                return []
            event = self.db.getEvent(self.eventCtrl.value)
            return [self.attendanceAsRow(athlete, event) for athlete in self.db.getAthletes(user.id)]
            
        def updateRows(e):
            self.table.rows = createRows()
            e.control.page.update()

        options = []
        for event in self.db.getAllEvents():
            options.append(
                ft.dropdownm2.Option(
                    key=event.id,
                    text=event.descr()
                )
            )

        self.eventCtrl = ft.Dropdown(
            editable=False,
            label="select event",
            options=options,
            width=400,
            on_change=updateRows
        )

        self.table = ft.DataTable(
                columns=[ft.DataColumn(ft.Text(h)) for h in header()],
            )
        self.controls = [
            ft.AppBar(title=ft.Text(f'Attendances of {user.team}'), bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST),
            self.eventCtrl,
            self.table,
            ft.Row(spacing=0, controls=[
                ft.IconButton(ft.Icons.SAVE,
                          icon_color=ft.Colors.BLUE_300,
                          tooltip="pdf",
                          on_click=printPdf)]),
            ft.ElevatedButton("Home", on_click=lambda _: self.page.go("/")),
        ]

    def attendanceAsRow(self, athlete: Athlete, event:Event):
        attendance = self.db.getAttendance(athlete.id, event.id)

        def onChange(e):
            msg = 'nominate' if e.control.value else 'denominate'
            print(f'{msg} {athlete.name()} for event {event.descr()}')

        checkBoxEnabled = event.progress == Progress.PLANNED
        checkBoxValue = attendance is not None

        cells = [
            ft.DataCell(ft.Checkbox(value=checkBoxValue, disabled=not checkBoxEnabled, on_change=onChange)),
            ft.DataCell(ft.Text(athlete.givenname)),
            ft.DataCell(ft.Text(athlete.surname)),
            ft.DataCell(ft.Text(athlete.birthFormated())),
            ft.DataCell(ft.Text(athlete.gender.name)),
            ]
        if attendance is not None:
            cells += [
                ft.DataCell(ft.Text(attendance.eventCategoryName)),
                ft.DataCell(ft.Text(attendance.group))
            ]
        else:
            cells += [
                ft.DataCell(ft.Text('')),
                ft.DataCell(ft.Text(''))
            ]
        return ft.DataRow(cells=cells)

