import os
import sys
import flet as ft
from view import View

sys.path.append(os.path.join(os.path.dirname(__file__), "../.."))
from shared.database import JuryDatabase, User, Athlete, Attendance, Gender, Event, Progress, Restrictions


def header():
    return ['', 'given name', 'surname', 'birth', 'gender', 'category', 'group']

class AttendanceView(View):
    def __init__(self, page: ft.Page, eventId: int):
        super().__init__(page)
        self.route = '/attendances/{eventId}'

        user = self.page.session.get('user')
        isHost = user.restrictions == Restrictions.HOST
        
        event = self.db.getEvent(eventId)
        
        def printPdf(e):
            host = self.page.url[5:]
            page.launch_url(f'https://api.{host}/attendances/{eventId}/{user.id}')

        def createRows():
            return [self.attendanceAsRow(attendance, deleteFunc) for attendance in self.db.getAttendances(event.id, user.id)]
            
        def updateRows():
            self.table.rows = self.createRows()


        def deleteFunc(e, athleteId):
            athlete = self.db.getAthlete(athleteId)
            def yes(e):
                self.db.removeAthlete(athleteId)
                dlg.open = False
                updateRows()
                e.control.page.update()

            def no(e):
                print('cancel')
                dlg.open = False
                e.control.page.update()

            dlg = ft.AlertDialog(
                modal=True,
                content=ft.Text(f"Delete attendance of athlete '{athlete.name()}'?"),
                actions=[
                    ft.TextButton("Yes", on_click=yes),
                    ft.TextButton("No", on_click=no),
                ],
                actions_alignment=ft.MainAxisAlignment.END)
            e.control.page.overlay.append(dlg)
            dlg.open = True
            e.control.page.update()

        self.table = ft.DataTable(
                columns=[ft.DataColumn(ft.Text(h)) for h in header()],
                rows=createRows()
            )
        self.controls = [
            ft.AppBar(title=ft.Text(f'Athletes of {user.team} attending {event.descr()}'), bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST),
            self.table,
            ft.Row(spacing=0, controls=[
                ft.IconButton(ft.Icons.SAVE,
                          icon_color=ft.Colors.BLUE_300,
                          tooltip="pdf",
                          on_click=printPdf)]),
            ft.ElevatedButton("Home", on_click=lambda _: self.page.go("/")),
        ]
        
    def attendanceAsRow(self, attendance: Attendance, deleteFunc: callable):
        athlete = self.db.getAthlete(attendance.athleteId)
        cells = [
            ft.DataCell(ft.IconButton(
                        icon=ft.Icons.DELETE,
                        icon_color=ft.Colors.RED_300,
                        tooltip="Delete",
                        on_click=lambda e: deleteFunc(e, athlete.id))),
            ft.DataCell(ft.Text(athlete.givenname)),
            ft.DataCell(ft.Text(athlete.surname)),
            ft.DataCell(ft.Text(athlete.birthFormated())),
            ft.DataCell(ft.Text(athlete.gender.name)),
            ft.DataCell(ft.Text(attendance.eventCategoryName)),
            ft.DataCell(ft.Text(attendance.group))
            ]
        return ft.DataRow(cells=cells)

