import os
import sys
import flet as ft
from view import View
from datetime import datetime

sys.path.append(os.path.join(os.path.dirname(__file__), "../.."))
from shared.database import JuryDatabase, Athlete, AthleteRatings, Gender

numFilter = ft.InputFilter(regex_string=r'^(\d+(\.\d*)?|\.\d+)$')

def formatPoints(value):
    if value is None:
        return '-----'
    return '{:.1f}'.format(value)

class RatingSelectEventView(View):
    def __init__(self, page: ft.Page, db, redis):
        super().__init__(page, db, redis)
        self.route = '/rating'

        self.controls = [
            ft.AppBar(title=ft.Text('Select Event'), bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST),
            ft.Container(
                content=ft.Column(
                    controls=[
                        ft.ElevatedButton(
                            f"{e.descr()}",
                            on_click=lambda _, id=e.id: self.page.go(f'/rating/{id}'),
                            width=300
                        ) for e in self.db.getAllEvents()
                    ],
                    scroll=ft.ScrollMode.AUTO,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=10
                ),
                expand=True,
                alignment=ft.alignment.center
            ),
            ft.ElevatedButton("Home", on_click=lambda _: self.page.go("/"))
        ]

class RatingView(View):
    def __init__(self, page: ft.Page, db, redis, eventId: int):
        super().__init__(page, db, redis)
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
        _, _, ratingId = ratings.ratingOrNone(discipline)
        def remove(e):
            self.db.removeRating(ratingId)
            self.updateControls()

        cells = [
            ft.DataCell(ft.Text(athlete.name())),
            ft.DataCell(ft.Text(ratings.eventCategoryName)),
            ft.DataCell(ft.Text('{:.1f}'.format(ratings.sum()))),
            ft.DataCell(ft.Text(ratings.prettyOrDefault(discipline))),
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
                    on_click=remove)]))
        ]
        return ft.DataRow(cells=cells)
        
    def updateControls(self):
        
        def editRating(e, ratings: AthleteRatings, discipline: str):
            print(f'edit athlete="{ratings.athlete.name()}"')
            difficultyContent, executionContent, ratingId = ratings.ratingOrNone(discipline)
            
            d_val = "{:.2f}".format(difficultyContent) if difficultyContent is not None else ""
            e_val = "{:.2f}".format(executionContent) if executionContent is not None else ""

            difficultyEdt = ft.TextField(label="difficulty", value=d_val, width=200, read_only=True, text_align=ft.TextAlign.RIGHT, border_color=ft.Colors.BLUE, border_width=2)
            executionEdt = ft.TextField(label="execution", value=e_val, width=200, read_only=True, text_align=ft.TextAlign.RIGHT)

            self.active_field = difficultyEdt

            def highlight_field(front, back):
                self.active_field = front
                front.border_width = 2
                front.border_color = None
                back.border_width = 1
                front.update()
                back.update()

            def set_difficulty(e):
                highlight_field(difficultyEdt, executionEdt)

            def set_execution(e):
                highlight_field(executionEdt, difficultyContent)

            difficultyEdt.on_focus = set_difficulty
            executionEdt.on_focus = set_execution

            def add_char(char):
                if self.active_field.value is None:
                    self.active_field.value = ""
                
                if self.active_field.value == "0" and char == "0":
                    return
                if self.active_field.value == "0" and char != ".":
                    self.active_field.value = char
                else:
                    self.active_field.value += char
                self.active_field.update()

            def backspace(e):
                if self.active_field.value and len(self.active_field.value) > 0:
                    self.active_field.value = self.active_field.value[:-1]
                    self.active_field.update()

            def digit_btn(digit):
                return ft.ElevatedButton(text=str(digit), on_click=lambda _: add_char(str(digit)), expand=1)

            keypad = ft.Column([
                ft.Row([digit_btn(7), digit_btn(8), digit_btn(9)], spacing=2),
                ft.Row([digit_btn(4), digit_btn(5), digit_btn(6)], spacing=2),
                ft.Row([digit_btn(1), digit_btn(2), digit_btn(3)], spacing=2),
                ft.Row([ft.ElevatedButton(".", on_click=lambda _: add_char("."), expand=1), digit_btn(0), ft.ElevatedButton(content=ft.Icon(ft.Icons.BACKSPACE_OUTLINED), on_click=backspace, expand=1)], spacing=2)
            ], spacing=2, width=200)

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
                            keypad,
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
                        tight=True, scroll=ft.ScrollMode.AUTO
                    ),
                    padding=10,
                )
            )
            self.page.overlay.append(self.dlg)
            self.page.update()
            self.page.open(self.dlg)

        
        self.table = ft.DataTable(
                columns=[ft.DataColumn(ft.Text(h)) for h in ['name', 'cat', 'sum', self.disciplineEdit.value, '']],
                rows= [self.AthleteRatingAsRow(athlete, self.disciplineEdit.value, editRating) for athlete in self.athletes],
                column_spacing=10,
                vertical_lines=ft.border.BorderSide(1, ft.Colors.OUTLINE)
            )

        self.controls = [
            ft.AppBar(title=ft.Text(f'Rating'), bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST),
            ft.Column(controls=[
                ft.Text(self.event.name, size=30, color=ft.Colors.PINK_600, italic=True),
                ft.Row([self.disciplineEdit, self.groupEdit], wrap=True),
                ft.Row([self.table], scroll=ft.ScrollMode.AUTO),
                ft.ElevatedButton("Home", on_click=lambda _: self.page.go("/"))
            ], scroll=ft.ScrollMode.AUTO, expand=True)
        ]
        self.page.update()
