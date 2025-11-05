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
        self.route = "/events"

        user = self.page.session.get('user')

        def addFunc(e):
            self.page.go("/eventEdit/0")

        def editFunc(e, eventId):
            self.page.go(f"/eventEdit/{eventId}")

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

        def createRows():
            return [eventAsRow(event, editFunc, deleteFunc) for event in self.db.getEvents(user.id)]

        self.table = ft.DataTable(
            columns=[ft.DataColumn(ft.Text(h)) for h in header()],
            rows=createRows()
        )

        self.controls = [
            ft.AppBar(title=ft.Text(f'Events of {user.username}'), bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST),
            self.table,
            ft.Row(
                spacing=0,
                controls=[
                    ft.IconButton(
                        ft.Icons.ADD_CIRCLE,
                        icon_color=ft.Colors.BLUE_300,
                        tooltip="Neues Event",
                        on_click=addFunc
                    )
                ]
            ),
            ft.ElevatedButton("Home", on_click=lambda _: self.page.go("/"))
        ]

class EventEditView(View):
    def __init__(self, page: ft.Page, eventId: int):
        super().__init__(page)
        self.route = f"/eventEdit/{eventId}"
        createEvent = eventId == 0

        if not page.session.contains_key("events_data"):
            page.session.set("events_data", [])
        events_data = page.session.get("events_data")

        event = next((ev for ev in events_data if ev["id"] == eventId), None)
        if event is None:
            event = {"id": eventId, "name": "", "date": ""}

        name_input = ft.TextField(label="Event Name", width=300, value=event["name"])
        date_input = ft.TextField(label="Datum (YYYY-MM-DD)", width=300, value=event["date"])

        def saveEvent(e):
            name = name_input.value.strip()
            date = date_input.value.strip()

            if not name or not date:
                self.page.open(ft.SnackBar(ft.Text("Bitte Name und Datum eingeben!"), bgcolor="red"))
                return

            if createEvent:
                new_id = max([ev["id"] for ev in events_data], default=0) + 1
                events_data.append({"id": new_id, "name": name, "date": date})
            else:
                for ev in events_data:
                    if ev["id"] == eventId:
                        ev["name"] = name
                        ev["date"] = date

            page.session.set("events_data", events_data)
            self.page.go("/events")

        def cancel(e):
            self.page.go("/events")

        self.controls = [
            ft.AppBar(title=ft.Text("Event erstellen" if createEvent else "Event bearbeiten"),
                      bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST),
            name_input,
            date_input,
            ft.Row(spacing=0, controls=[
                ft.IconButton(icon=ft.Icons.CHECK_CIRCLE, icon_color=ft.Colors.GREEN_300, tooltip="Speichern", on_click=saveEvent),
                ft.IconButton(icon=ft.Icons.CANCEL, icon_color=ft.Colors.RED_300, tooltip="Abbrechen", on_click=cancel),
            ]),
        ]
