import flet as ft
import pymysql.cursors
from database import JuryDatabase, Athlete

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
        ft.DataCell(ft.Text(athlete.birth)),
        ft.DataCell(ft.Text(athlete.gender.name))
        ]
    return ft.DataRow(cells=cells)

class AthleteView(ft.View):
    def __init__(self, page: ft.Page):
        super().__init__()
        self.page = page
        self.route = '/athletes'
        db = JuryDatabase('db')

        user = db.getUser(self.page.session.get('userId'))
        
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
                content=ft.Text(f"Delete athlete '{athlete.name}'?"),
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
            self.page.go(f'/athleteEdit/{userId}')
        
        def addFunc(e):
            self.page.go(f'/athleteEdit/0')
            
        self.table = ft.DataTable(
                columns=[ft.DataColumn(ft.Text(h)) for h in header()],
                rows=[athleteAsRow(athlete, editFunc, deleteFunc) for athlete in db.getAthletes(user.id)]
            )
        self.controls = [
            ft.AppBar(title=ft.Text(f'Athletes of {user.team}'), bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST),
            self.table,
            ft.IconButton(ft.Icons.ADD_CIRCLE,
                    icon_color=ft.Colors.BLUE_300,
                    tooltip="Add",
                    on_click=addFunc),
            ft.ElevatedButton("Home", on_click=lambda _: self.page.go("/")),
        ]

    def did_mount(self):
        print('Did mount')
        self.update()

    def will_unmount(self):
        print('Will unmount')

