import os
import sys
import flet as ft

sys.path.append(os.path.join(os.path.dirname(__file__), "../.."))
from shared.database import JuryDatabase, Athlete, Gender


class RatingView(ft.View):
    def __init__(self, page: ft.Page, eventId: int):
        super().__init__()
        self.page = page
        self.route = f'/rating/{eventId}'
        self.db = JuryDatabase('db')

        self.user = self.page.session.get('user')
        self.event = self.db.getEvent(eventId)
        self.disciplines = self.db.getEventDisciplines(eventId)
        self.groups = self.db.getEventGroups(eventId)
        self.athletes = []
        
        def updateAthletes(e):
            self.athletes = self.db.getEventGroup(self.event.id, self.groupEdit.value)
            self.updateControls()

        self.disciplineEdit = ft.Dropdown(
            label="Discipline",
            width = 300,
            options=[ft.dropdownm2.Option(d.name) for d in self.disciplines],
            on_change=updateAthletes
        )
        self.groupEdit = ft.Dropdown(
            label="Group",
            width = 300,
            options=[ft.dropdownm2.Option(g) for g in self.groups],
            on_change=updateAthletes
        )
        self.updateControls()

        
    def updateControls(self):
        self.controls = [
            ft.AppBar(title=ft.Text(f'Rating'), bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST),
            ft.Text(self.event.name, size=30, color=ft.Colors.PINK_600, italic=True),
            self.disciplineEdit,
            self.groupEdit]
        
        for athlete in self.athletes:
            self.controls.append(
                ft.Text(value=athlete.name())
            )         
        self.controls.append(
            ft.ElevatedButton("Home", on_click=lambda _: self.page.go("/")))
        self.page.update()


