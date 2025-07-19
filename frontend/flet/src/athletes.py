import os
import sys
import flet as ft

sys.path.append(os.path.join(os.path.dirname(__file__), "../.."))
from shared.database import JuryDatabase, Athlete, Gender


def header():
    return ['', '', 'given name', 'surname', 'birth', 'gender']

def athleteAsRow(athlete: Athlete, editFunc: callable, deleteFunc: callable):
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

class AthleteView(ft.View):
    def __init__(self, page: ft.Page):
        super().__init__()
        self.page = page
        self.route = '/athletes'
        db = JuryDatabase('db')

        user = self.page.session.get('user')
        
        def deleteFunc(e, athleteId):
            athlete = db.getAthlete(athleteId)
            def yes(e):
                db.removeAthlete(athleteId)
                dlg.open = False
                self.table.rows = [athleteAsRow(athlete, editFunc, deleteFunc) for athlete in db.getAthletes(user.id)]
                e.control.page.update()

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
            host = self.page.url[5:]
            page.launch_url(f'https://api.{host}/athletes/{user.id}')
            
        self.table = ft.DataTable(
                columns=[ft.DataColumn(ft.Text(h)) for h in header()],
                rows=[athleteAsRow(athlete, editFunc, deleteFunc) for athlete in db.getAthletes(user.id)]
            )
        self.controls = [
            ft.AppBar(title=ft.Text(f'Athletes of {user.team}'), bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST),
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

    def did_mount(self):
        print('Did mount')
        self.update()

    def will_unmount(self):
        print('Will unmount')


class AthleteEditView(ft.View):
    def __init__(self, page: ft.Page, athleteId: int):
        super().__init__()
        self.page = page
        self.route = f'/athleteEdit/{athleteId}'
        db = JuryDatabase('db')
        createAthlete = athleteId == 0
        user = self.page.session.get('user')
        
        def update(e):
            if createAthlete:
                print(f'creating athlete')
                db.insertAthlete(givenNameEdit.value, surnameEdit.value, user.id, birthEdit.value, Gender[genderEdit.value])
            else:
                print(f'saving {athleteId=}')
                db.updateAthlete(athleteId, givenNameEdit.value, surnameEdit.value, user.id, birthEdit.value, Gender[genderEdit.value])
            self.page.go("/athletes")
            
        def cancel(e):
            print(f'cancel {athleteId=}')
            self.page.go("/athletes")

        print(f'get athlete {athleteId=}')
        if not createAthlete:
            athlete = db.getAthlete(athleteId)
            print(f'edit {athlete.name()}')
        givenNameEdit = ft.TextField(label="given name", value=None if createAthlete else athlete.givenname)
        surnameEdit = ft.TextField(label="surname", value=None if createAthlete else athlete.surname)
        teamEdit = ft.TextField(label="Team", value=user.team, disabled=True)
        birthEdit = ft.TextField(label="birth", value=None if createAthlete else athlete.birthFormated())
        genderEdit = ft.Dropdown(
            label="gender",
            width = 300,
            options=[ft.dropdownm2.Option(e.name) for e in Gender],
            value=Gender.FEMALE.name if createAthlete else athlete.gender.name)
        self.controls = [
            ft.AppBar(title=ft.Text(f'{'Create ' if createAthlete else 'Edit '} Athlete'), bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST),
            givenNameEdit,
            surnameEdit,
            teamEdit,
            birthEdit,
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
