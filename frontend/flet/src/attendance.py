import os
import sys
import flet as ft
from view import View

sys.path.append(os.path.join(os.path.dirname(__file__), "../.."))
from shared.database import JuryDatabase, User, Athlete, Attendance, Gender, Event, Progress, Restrictions


def header():
    return ['', 'given name', 'surname', 'birth', 'gender', 'category', 'group']

class AttendanceView(View):
    def user(self) -> User:
        return self.page.session.get('user')
    
    def __init__(self, page: ft.Page):
        super().__init__(page)
        self.route = '/attendances'

        def printPdf(e):
            if self.eventCtrl.value is None:
                return
            eventId = self.eventCtrl.value
            host = self.page.url[5:]
            page.launch_url(f'https://api.{host}/attendances/{self.user().id}/{eventId}')

        def createRows():
            if self.eventCtrl.value is None:
                return []
            event = self.db.getEvent(self.eventCtrl.value)
            categories = self.db.getEventCategories(event.id)
            athletes = []
            if self.user().isHost():
                for attendance in self.db.getEventAttendances(event.id):
                    athletes.append(self.db.getAthlete(attendance.athleteId))
            else:
                athletes = self.db.getAthletes(self.user().id)
            return [self.attendanceAsRow(athlete, event, categories) for athlete in athletes]
            
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
        title = f'Attendances of {self.user().username if self.user().isHost() else self.user().team}'
        self.controls = [
            ft.AppBar(title=ft.Text(title), bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST),
            self.eventCtrl,
            self.table,
            ft.Row(spacing=0, controls=[
                ft.IconButton(ft.Icons.SAVE,
                          icon_color=ft.Colors.BLUE_300,
                          tooltip="pdf",
                          on_click=printPdf)]),
            ft.ElevatedButton("Home", on_click=lambda _: self.page.go("/")),
        ]

    def attendanceAsRow(self, athlete: Athlete, event:Event, categories: list):
        def onChange(e):
            attendance = self.db.getAttendance(athlete.id, event.id)
            if e.control.value:
                print(f'nominate {athlete.name()} for {event.descr()}')
                if attendance:
                    categoryCell.content.value = attendance.eventCategoryName
                    groupCell.content.value = attendance.group
                    groupCell.content.disabled = not self.user().isHost()
                else:
                    groupCell.content.disabled = True
                categoryCell.content.disabled = False
                categoryCell.content.options = [ft.dropdownm2.Option(d.name) for d in categories]
            else:
                print(f'denominate {athlete.name()} for {event.descr()}')
                self.db.hideAttendance(event.id, athlete.id, True)
                categoryCell.content.value = ''
                groupCell.content.value = ''
                categoryCell.content.disabled = True
                groupCell.content.disabled = True
                categoryCell.content.options = []
            self.page.update()

        def onUpdateCategory(e):
            self.db.setAttendanceCategory(event.id, athlete.id, e.control.value)
            groupCell.content.disabled = not self.user().isHost()
            self.page.update()

        def onUpdateGroup(e):
            self.db.setAttendanceGroup(event.id, athlete.id, e.control.value)

        attendance = self.db.getAttendance(athlete.id, event.id)
        checkBoxEnabled = event.progress() == Progress.PLANNED
        checkBoxValue = attendance is not None
        categoryCell = ft.DataCell(ft.Dropdown(
                    disabled=not attendance,
                    options=list() if attendance is None else [ft.dropdownm2.Option(d.name) for d in categories],
                    value=attendance.eventCategoryName if attendance else None,
                    on_change=onUpdateCategory
                    ))
        groupCell = ft.DataCell(ft.TextField(
                    disabled=not attendance or not self.user().isHost(),
                    value=attendance.group if attendance else None,
                    on_change=onUpdateGroup,
                    expand=True,
                    ))
        cells = [
            ft.DataCell(ft.Checkbox(value=checkBoxValue, disabled=not checkBoxEnabled, on_change=onChange)),
            ft.DataCell(ft.Text(athlete.givenname)),
            ft.DataCell(ft.Text(athlete.surname)),
            ft.DataCell(ft.Text(athlete.birthFormated())),
            ft.DataCell(ft.Text(athlete.gender.name)),
            categoryCell,
            groupCell
            ]
        return ft.DataRow(cells=cells)

