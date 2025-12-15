import os
import sys
import flet as ft
from view import View
from datetime import datetime

sys.path.append(os.path.join(os.path.dirname(__file__), "../.."))
from shared.database import JuryDatabase, Athlete, AthleteRatings, Gender

numFilter = ft.InputFilter(regex_string=r'^(\d+(\.\d*)?|\.\d+)$')

def emptyIfNone(o):
    return '-----' if o is None else o
class RatingView(View):
    def __init__(self, page: ft.Page, eventId: int):
        super().__init__(page)
        self.route = f'/rating/{eventId}'

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

    def AthleteRatingAsRow(self, athlete: Athlete, discipline: str, editFunc: callable):
        ratings = self.db.getAthleteAndRatings(athlete.id, self.event.id)
        difficultyText, executionText, ratingId = ratings.ratingOrNone(discipline)
        cells = [
            ft.DataCell(ft.Text(athlete.name())),
            ft.DataCell(ft.Text(ratings.eventCategoryName)),
            ft.DataCell(ft.Text('{:.1f}'.format(ratings.sum()))),
            ft.DataCell(ft.Text('-----' if difficultyText is None else '{:.1f}'.format(difficultyText))),
            ft.DataCell(ft.Text('-----' if executionText is None else '{:.1f}'.format(executionText))),
            ft.DataCell(ft.Row(spacing=0, controls=[
                ft.IconButton(
                    icon=ft.Icons.EDIT,
                    icon_color=ft.Colors.GREEN_300,
                    tooltip="Edit Rating",
                    on_click=lambda e: editFunc(e, ratings, discipline)),
                ft.IconButton(
                    icon=ft.Icons.DELETE,
                    icon_color=ft.Colors.RED_300,
                    tooltip="Delete",
                    on_click=lambda e: self.db.removeRating(ratingId))]))
        ]
        return ft.DataRow(cells=cells)
        
    def updateControls(self):
        
        def editRating(e, ratings: AthleteRatings, discipline: str):
            print(f'edit athlete="{ratings.athlete.name()}"')
            difficultyContent, executionContent, ratingId = ratings.ratingOrNone(discipline)
            difficultyEdt = ft.TextField(label="difficulty", value=difficultyContent, width=200, input_filter=numFilter)
            executionEdt = ft.TextField(label="execution", value=executionContent, width=200, input_filter=numFilter)

            def update(e):
                print(f'update athlete="{ratings.athlete.name()}"')
                if ratingId is None:
                    self.db.insertRating(ratings.athlete.id, ratings.eventId,
                                         self.user.id, self.disciplineEdit.value,
                                         difficultyEdt.value, executionEdt.value)
                else:
                    self.db.updateRating(ratingId, self.user.id, difficultyEdt.value,
                                         executionEdt.value)
                self.page.close(self.dlg)
                self.updateControls()
            def cancel(e):
                print(f'cancel athlete="{ratings.athlete.name()}"')
                self.page.close(self.dlg)

            self.dlg = ft.AlertDialog(
                modal=True,
                content=ft.Container(
                    ft.Column(
                        [
                            ft.Text(discipline),
                            ft.Text(ratings.athlete.name()),
                            ft.Text(f'{ratings.eventCategoryName} {ratings.athlete.birthFormated()}'),
                            difficultyEdt,
                            executionEdt,
                            ft.Row(spacing=0, controls=
                                [
                                    ft.IconButton(
                                        icon=ft.Icons.CHECK_CIRCLE,
                                        icon_color=ft.Colors.GREEN_300,
                                        tooltip="Save",
                                        on_click=update),
                                    ft.IconButton(
                                        icon=ft.Icons.CANCEL,
                                        icon_color=ft.Colors.RED_300,
                                        tooltip="Cancel",
                                        on_click=cancel)
                                ], alignment=ft.MainAxisAlignment.CENTER)
                        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        tight=True,
                    ),
                    padding=20,
                )
            )
            self.page.overlay.append(self.dlg)
            self.page.update()
            self.page.open(self.dlg)

        
        self.table = ft.DataTable(
                columns=[ft.DataColumn(ft.Text(h)) for h in ['name', 'cat', 'sum', self.disciplineEdit.value, '', '']],
                rows= [self.AthleteRatingAsRow(athlete, self.disciplineEdit.value, editRating) for athlete in self.athletes],
                column_spacing=10,
                vertical_lines=ft.border.BorderSide(1, ft.Colors.OUTLINE)
            )

        self.controls = [
            ft.AppBar(title=ft.Text(f'Rating'), bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST),
            ft.Text(self.event.name, size=30, color=ft.Colors.PINK_600, italic=True),
            self.disciplineEdit,
            self.groupEdit,
            self.table,
            ft.ElevatedButton("Home", on_click=lambda _: self.page.go("/"))]
        self.page.update()
