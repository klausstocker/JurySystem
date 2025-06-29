import flet as ft
import pymysql.cursors


class UserView(ft.View):
    def __init__(self, page: ft.Page):
        super().__init__()
        self.conn = pymysql.connect(host='db',
                             user='JurySystem',
                             password='asdfuas347lkasudhr',
                             database='JurySystem',
                             cursorclass=pymysql.cursors.DictCursor)
        with self.conn:
            with self.conn.cursor() as cursor:
                columns = cursor.execute('SHOW COLUMNS FROM users;')
                print(columns)
        self.page = page
        self.route = '/users'
        self.controls = [
            ft.AppBar(title=ft.Text("Users"), bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST),
            ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("Vorname")),
                ft.DataColumn(ft.Text("Nachname")),
                ft.DataColumn(ft.Text("Geburtsdatum")),
            ],
            ),
            ft.ElevatedButton("Home", on_click=lambda _: self.page.go("/")),
        ]

    def did_mount(self):
        print('Did mount')
        self.update()

    def will_unmount(self):
        print('Will unmount')
