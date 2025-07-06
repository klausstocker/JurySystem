import flet as ft
from navigation import Navigator
from database import JuryDatabase

def main(page: ft.Page):
    page.title = "Jury System"
    jurydb = JuryDatabase('db')

    def loginbtn(e):
        userId = jurydb.validateUser(username.value, password.value)
        if userId is not None:
            print("Redirecting...")
            navi = Navigator(page)
            page.session.set("userId", userId)
            page.on_route_change = navi.route_change
            page.on_view_pop = navi.view_pop
            page.go(page.route)
        else:
            print("Login failed !!!")
            page.open(ft.SnackBar(
                ft.Text("wrong login, user expired or locked", size=30),
                bgcolor="red"
            ))

    username = ft.TextField(label="User name")
    password = ft.TextField(label="Password", password=True, can_reveal_password=True, on_submit=loginbtn)
    
    page.theme_mode = ft.ThemeMode.DARK
    page.auto_scroll = True
    page.controls = [username, password,ft.ElevatedButton("Login Now",
                                  bgcolor="blue", color="white",
                                  on_click=loginbtn)]
    page.update()

ft.app(main, assets_dir="assets")

