import os
import sys
import datetime
import flet as ft
from view import View

sys.path.append(os.path.join(os.path.dirname(__file__), "../.."))
from shared.database import JuryDatabase, Athlete, Gender, Event, Progress


def header():
    return ['', '', 'given name', 'surname', 'birth', 'gender']

class AthleteView(View):
    def __init__(self, page: ft.Page, db, redis):
        super().__init__(page, db, redis)
        self.route = '/athletes'

        user = self.page.session.get('user')

        def createRows():
            return [self.athleteAsRow(athlete, editFunc, deleteFunc) for athlete in self.db.getAthletes(user.id)]

        def updateRows(e):
            self.table.rows = createRows()
            e.control.page.update()

        def deleteFunc(e, athleteId):
            athlete = self.db.getAthlete(athleteId)
            def yes(e):
                self.db.removeAthlete(athleteId)
                dlg.open = False
                updateRows(e)

            def no(e):
                print('cancel')
                dlg.open = False
                e.control.page.update()

            dlg = ft.AlertDialog(
                modal=True,
                content=ft.Text(f"Delete athlete '{athlete.name()}'?"),
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
            self.page.go(f'/athleteEdit/{athleteId}')
        
        def addFunc(e):
            self.page.go(f'/athleteEdit/0')
            
        def printPdf(e):
            page.launch_url(f'https://{View.api()}/athletes/{user.id}')

        self.table = ft.DataTable(
                columns=[ft.DataColumn(ft.Text(h)) for h in header()],
                rows=createRows()
            )
        self.controls = [
            ft.AppBar(leading=ft.IconButton(icon=ft.Icons.HELP_OUTLINE, tooltip="Help", on_click=lambda _: self.page.go('/help')), title=ft.Text(f'Athletes of {user.team}'), bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST),
            self.table,
            ft.Row(spacing=0, controls=[
                ft.IconButton(ft.Icons.ADD_CIRCLE,
                    icon_color=ft.Colors.BLUE_300,
                    tooltip="Add",
                    on_click=addFunc),
                ft.IconButton(ft.Icons.SAVE,
                          icon_color=ft.Colors.BLUE_300,
                          tooltip="pdf",
                          on_click=printPdf)]),
            ft.ElevatedButton("Home", on_click=lambda _: self.page.go("/")),
        ]
        
    def athleteAsRow(self, athlete: Athlete, editFunc: callable, deleteFunc: callable):
        cells = [
            ft.DataCell(ft.IconButton(
                        icon=ft.Icons.EDIT,
                        icon_color=ft.Colors.GREEN_300,
                        tooltip="Edit",
                        on_click=lambda e: editFunc(e, athlete.id))),
            ft.DataCell(ft.IconButton(
                        icon=ft.Icons.DELETE,
                        icon_color=ft.Colors.RED_300,
                        tooltip="Delete",
                        on_click=lambda e: deleteFunc(e, athlete.id))),
            ft.DataCell(ft.Text(athlete.givenname)),
            ft.DataCell(ft.Text(athlete.surname)),
            ft.DataCell(ft.Text(athlete.birthFormated())),
            ft.DataCell(ft.Text(athlete.gender.name))
            ]
        return ft.DataRow(cells=cells)



class AthleteEditView(View):
    def __init__(self, page: ft.Page, db, redis, athleteId: int):
        super().__init__(page, db, redis)
        self.route = f'/athleteEdit/{athleteId}'
        createAthlete = athleteId == 0
        user = self.page.session.get('user')
        
        def update(e):
            if createAthlete:
                print(f'creating athlete')
                self.db.insertAthlete(givenNameEdit.value, surnameEdit.value, user.id, Athlete.birthFromString(self.birthEdit.value), Gender[genderEdit.value])
            else:
                print(f'saving {athleteId=}')
                self.db.updateAthlete(athleteId, givenNameEdit.value, surnameEdit.value, user.id, Athlete.birthFromString(self.birthEdit.value), Gender[genderEdit.value])
            self.page.go("/athletes")
            
        def cancel(e):
            print(f'cancel {athleteId=}')
            self.page.go("/athletes")

        def onChangeBirth(e):
            self.birthEdit.value = e.control.value.strftime("%d.%m.%Y")
            self.page.update()

        print(f'get athlete {athleteId=}')
        if not createAthlete:
            athlete = self.db.getAthlete(athleteId)
            birth_value = athlete.birthFormated()
        else:
            birth_value = ""
        givenNameEdit = ft.TextField(label="Given name", value=None if createAthlete else athlete.givenname)
        surnameEdit = ft.TextField(label="Surname", value=None if createAthlete else athlete.surname)
        teamEdit = ft.TextField(label="Team", value=user.team, disabled=True)
        self.birthEdit = ft.TextField(
            label="Birth",
            value=birth_value,
            disabled=True,
            width=115
        )
        birthPicker = ft.ElevatedButton(
            "Pick date",
            icon=ft.Icons.CALENDAR_MONTH,
            on_click=lambda e: page.open(
                ft.DatePicker(
                    first_date=datetime.datetime(year=1980, month=1, day=1),
                    last_date=datetime.datetime(year=2025, month=12, day=31),
                    on_change = onChangeBirth
                )
            ),
        )
        birth_row = ft.Row(
            controls=[
                self.birthEdit,
                birthPicker
            ],
            spacing=10,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        )
        
    
        genderEdit = ft.Dropdown(
            label="gender",
            width = 300,
            options=[ft.dropdownm2.Option(e.name) for e in Gender],
            value=Gender.FEMALE.name if createAthlete else athlete.gender.name)
        self.controls = [
            ft.AppBar(leading=ft.IconButton(icon=ft.Icons.HELP_OUTLINE, tooltip="Help", on_click=lambda _: self.page.go('/help')), title=ft.Text(f'{'Create ' if createAthlete else 'Edit '} Athlete'), bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST),
            givenNameEdit,
            surnameEdit,
            teamEdit,
            birth_row,
            genderEdit,
            ft.Row(spacing=0, controls=[
                    ft.IconButton(
                        icon=ft.Icons.CHECK_CIRCLE,
                        icon_color=ft.Colors.GREEN_300,
                        tooltip="Save",
                        on_click=update),
                    ft.IconButton(
                        icon=ft.Icons.CANCEL,
                        icon_color=ft.Colors.RED_300,
                        tooltip="Cancel",
                        on_click=cancel)], scroll=ft.ScrollMode.AUTO),
            ft.ElevatedButton("Home", on_click=lambda _: self.page.go("/"))
            ]
