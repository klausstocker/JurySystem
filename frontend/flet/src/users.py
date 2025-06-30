import flet as ft
import pymysql.cursors
from database import JuryDatabase, User

def header():
    return ['', '', 'Username', 'E-Mail', 'registriert', 'läuft ab', 'Berechtigung', 'gesperrt']

def userAsRow(user: User, editFunc: callable, deleteFunc: callable):
    cells = [
        ft.DataCell(ft.IconButton(
                    icon=ft.Icons.EDIT,
                    icon_color=ft.Colors.GREEN_300,
                    tooltip="Edit",
                    on_click=lambda e: editFunc(user.id))),
        ft.DataCell(ft.IconButton(
                    icon=ft.Icons.DELETE,
                    icon_color=ft.Colors.RED_300,
                    tooltip="Delete",
                    on_click=lambda e: deleteFunc(user.id))),
        ft.DataCell(ft.Text(user.username)),
        ft.DataCell(ft.Text(user.email)),
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
        
        def deleteFunc(userId):
            db.removeUser(userId)
        
        def editFunc(userId):
            print(f'edit {userId=}')
        
        users = db.getAllUsers()
        self.page = page
        self.route = '/users'
        self.controls = [
            ft.AppBar(title=ft.Text("Users"), bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST),
            ft.DataTable(
                columns=[ft.DataColumn(ft.Text(h)) for h in header()],
                rows=[userAsRow(user, editFunc, deleteFunc) for user in users]
            ),
            ft.ElevatedButton("Home", on_click=lambda _: self.page.go("/")),
        ]

    def did_mount(self):
        print('Did mount')
        self.update()

    def will_unmount(self):
        print('Will unmount')
