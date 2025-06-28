import flet as ft
from navigation import Navigator

def main(page: ft.Page):
    page.title = "Jury System"

    username = ft.TextField(label="User name")
    password = ft.TextField(label="Password")

    def loginbtn(e):
        data = {"users": [
            {"name": "admin", "password": "adminpass"}, 
            {"name": "user", "password": "user"}, 
            ]}

        found = False
        for user in data["users"]:
            if user['name'] == username.value and user['password'] == password.value:
                found = True
                print("Login success !!!")
                break

        if found:
            print("Redirecting...")
            navi = Navigator(page)
            page.session.set("username", username.value)
            page.on_route_change = navi.route_change
            page.on_view_pop = navi.view_pop
            page.go(page.route)
        else:
            print("Login failed !!!")
            page.open(ft.SnackBar(
                ft.Text("Wrong login", size=30),
                bgcolor="red"
            ))

    page.theme_mode = ft.ThemeMode.DARK
    page.auto_scroll = True
    page.controls = [username, password,ft.ElevatedButton("Login Now",
                                  bgcolor="blue", color="white",
                                  on_click=loginbtn)]
    page.update()

ft.app(main, assets_dir="assets")

