import os
import sys
import flet as ft
from view import View

sys.path.append(os.path.join(os.path.dirname(__file__), "../.."))
from shared.database import JuryDatabase, Event


def header():
    return ['', '', 'name', 'date', 'progress']

def eventAsRow(event: Event, editFunc: callable, deleteFunc: callable):
    cells = [
        ft.DataCell(ft.IconButton(
                    icon=ft.Icons.EDIT,
                    icon_color=ft.Colors.GREEN_300,
                    tooltip="Edit",
                    on_click=lambda e: editFunc(e, event.id))),
        ft.DataCell(ft.IconButton(
                    icon=ft.Icons.DELETE,
                    icon_color=ft.Colors.RED_300,
                    tooltip="Delete",
                    on_click=lambda e: deleteFunc(e, event.id))),
        ft.DataCell(ft.Text(event.name)),
        ft.DataCell(ft.Text(event.dateFormated())),
        ft.DataCell(ft.Text(event.progress))
        ]
    return ft.DataRow(cells=cells)

class EventView(View):
    def __init__(self, page: ft.Page):
        super().__init__(page)
        self.route = '/events'
        print("test")
        user = self.page.session.get('user')
        
        def createRows():
            return [eventAsRow(event, editFunc, deleteFunc) for event in self.db.getEvents(user.id)]
        
        def deleteFunc(e, eventId):
            event = self.db.getEvent(eventId)
            def yes(e):
                self.db.removeEvent(eventId)
                dlg.open = False
                self.table.rows = createRows()
                e.control.page.update()

            def no(e):
                print('cancel')
                dlg.open = False
                e.control.page.update()

            dlg = ft.AlertDialog(
                modal=True,
                content=ft.Text(f"Delete event {event.descr()} ?"),
                actions=[
                    ft.TextButton("Yes", on_click=yes),
                    ft.TextButton("No", on_click=no),
                ],
                actions_alignment=ft.MainAxisAlignment.END)
            e.control.page.overlay.append(dlg)
            dlg.open = True
            e.control.page.update()

        def editFunc(e, athleteId):
            print(f'edit {athleteId=}')
            #self.page.go(f'/athleteEdit/{athleteId}')
        
        def addFunc(e):
            print(f'add event')
            #self.page.go(f'/athleteEdit/0')
            
        #def printPdf(e):
        #    host = self.page.url[5:]
        #    page.launch_url(f'https://api.{host}/athletes/{user.id}')
            
        self.table = ft.DataTable(
                columns=[ft.DataColumn(ft.Text(h)) for h in header()],
                rows=createRows()
            )
        self.controls = [
            ft.AppBar(title=ft.Text(f'Events of {user.username}'), bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST),
            self.table,
            ft.Row(spacing=0, controls=[
                ft.IconButton(ft.Icons.ADD_CIRCLE,
                    icon_color=ft.Colors.BLUE_300,
                    tooltip="Add",
                    on_click=addFunc)]),
            ft.ElevatedButton("Home", on_click=lambda _: self.page.go("/")),
        ]


