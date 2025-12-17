import os
import sys
import flet as ft
from view import View

sys.path.append(os.path.join(os.path.dirname(__file__), "../.."))
from shared.database import JuryDatabase, User, Restrictions

def header():
    return ['', '', 'Username', 'E-Mail', 'Team', 'registriert', 'läuft ab', 'Berechtigung', 'gesperrt', 'qr', '']

class UserView(View):
    def __init__(self, page: ft.Page, db, redis):
        super().__init__(page, db, redis)

        def createRows():
            return [self.userAsRow(user, editFunc, deleteFunc) for user in self.db.getAllUsers()]
        
        def deleteFunc(e, userId):
            user = self.db.getUser(userId)
            def yes(e):
                self.db.removeUser(userId)
                dlg.open = False
                self.table.rows = createRows()
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
            self.page.go(f'/userEdit/{userId}')
        
        def addFunc(e):
            self.page.go(f'/userEdit/0')
            
        self.page = page
        self.route = '/users'
        self.table = ft.DataTable(
                columns=[ft.DataColumn(ft.Text(h)) for h in header()],
                rows=createRows()
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
        
    def userAsRow(self, user: User, editFunc: callable, deleteFunc: callable):
        def downlodQR(e):
            e.page.launch_url(f'https://{View.api()}/qrcodes/login/{self.token()}/{user.id}')

        def recreateQr(e):
            self.db.recreateUserToken(user.id)

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
            ft.DataCell(ft.Checkbox(value=user.locked, disabled=True)),
            ft.DataCell(ft.IconButton(
                icon=ft.Icons.QR_CODE_2_ROUNDED,
                tooltip="qr-code for token login",
                on_click=downlodQR)),
            ft.DataCell(ft.IconButton(
                icon=ft.Icons.AUTORENEW_ROUNDED,
                tooltip="renew token for qr-code login",
                on_click=recreateQr))
            ]
        return ft.DataRow(cells=cells)

class UserEditView(View):
    def __init__(self, page: ft.Page, db, redis, userId: int):
        super().__init__(page, db, redis)
        self.route = f'/userEdit/{userId}'

        createUser = userId == 0

        def update(e):
            if createUser:
                print(f'creating user')
                self.db.insertUser(nameEdit.value, passwordEdit.value, emailEdit.value, teamEdit.value, Restrictions[resitrictionsEdit.value])
            else:
                print(f'saving {userId=}')
                self.db.updateUser(userId, nameEdit.value, passwordEdit.value, emailEdit.value, teamEdit.value, expiresEdit.value, Restrictions[resitrictionsEdit.value], lockedEdit.value)
            self.page.go("/users")

        def cancel(e):
            print(f'cancel {userId=}')
            self.page.go("/users")

        print(f'get user {userId=}')
        if not createUser:
            user = self.db.getUser(userId)
            print(f'{user.username=}')
        nameEdit = ft.TextField(label="Username", value=None if createUser else user.username)
        passwordEdit = ft.TextField(label="Passworde", value=None if createUser else user.password)
        emailEdit = ft.TextField(label="Email", value=None if createUser else user.email)
        teamEdit = ft.TextField(label="Team", value=None if createUser else user.team)
        resitrictionsEdit = ft.Dropdown(
            label="Restrictions",
            width = 300,
            options=[ft.dropdownm2.Option(e.name) for e in Restrictions],
            value=Restrictions.TRAINER.name if createUser else user.restrictions.name)
        expiresEdit = ft.TextField(label="expires", value=None if createUser else user.expires)
        lockedEdit = ft.Checkbox(label="locked", value=False if createUser else user.locked)
        self.controls = [
            ft.AppBar(title=ft.Text(f'{'Create ' if createUser else 'Edit '} User'), bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST),
            nameEdit,
            passwordEdit,
            emailEdit,
            teamEdit,
            resitrictionsEdit]
        if not createUser:
            self.controls += [
                expiresEdit,
                lockedEdit
            ]
        self.controls += [
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
                        on_click=cancel)], scroll=ft.ScrollMode.AUTO),
            ft.ElevatedButton("Home", on_click=lambda _: self.page.go("/"))
        ]

