import flet as ft
import pymysql.cursors
from database import JuryDatabase, User

def header():
    return ['', '', 'Username', 'E-Mail', 'Team', 'registriert', 'läuft ab', 'Berechtigung', 'gesperrt']

def userAsRow(user: User, editFunc: callable, deleteFunc: callable):
    cells = [
        ft.DataCell(ft.IconButton(
                    icon=ft.Icons.EDIT,
                    icon_color=ft.Colors.GREEN_300,
                    tooltip="Edit",
                    on_click=lambda e: editFunc(e, user.id))),
        ft.DataCell(ft.IconButton(
                    icon=ft.Icons.DELETE,
                    icon_color=ft.Colors.RED_300,
                    tooltip="Delete",
                    on_click=lambda e: deleteFunc(e, user.id))),
        ft.DataCell(ft.Text(user.username)),
        ft.DataCell(ft.Text(user.email)),
        ft.DataCell(ft.Text(user.team)),
        ft.DataCell(ft.Text(user.registered)),
        ft.DataCell(ft.Text(user.expires)),
        ft.DataCell(ft.Text(user.restrictions.name)),
        ft.DataCell(ft.Checkbox(value=user.locked, disabled=True))
        ]
    return ft.DataRow(cells=cells)

class UserView(ft.View):
    def __init__(self, page: ft.Page):
        super().__init__()
        db = JuryDatabase('db')
        
        def deleteFunc(e, userId):
            user = db.getUser(userId)
            def yes(e):
                db.removeUser(userId)
                dlg.open = False
                self.table.rows = [userAsRow(user, editFunc, deleteFunc) for user in db.getAllUsers()]
                e.control.page.update()

            def no(e):
                print('cancel')
                dlg.open = False
                e.control.page.update()

            dlg = ft.AlertDialog(
                modal=True,
                content=ft.Text(f"Delete user '{user.username}'?"),
                actions=[
                    ft.TextButton("Yes", on_click=yes),
                    ft.TextButton("No", on_click=no),
                ],
                actions_alignment=ft.MainAxisAlignment.END)
            e.control.page.overlay.append(dlg)
            dlg.open = True
            e.control.page.update()

        def editFunc(e, userId):
            print(f'edit {userId=}')
        
        def addFunc(e):
            print('add')
        
        self.page = page
        self.route = '/users'
        self.table = ft.DataTable(
                columns=[ft.DataColumn(ft.Text(h)) for h in header()],
                rows=[userAsRow(user, editFunc, deleteFunc) for user in db.getAllUsers()]
            )
        self.controls = [
            ft.AppBar(title=ft.Text("Users"), bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST),
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
