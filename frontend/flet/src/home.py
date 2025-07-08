import flet as ft
from database import JuryDatabase

class HomeView(ft.View):
    def __init__(self, page: ft.Page):
        super().__init__()
        self.page = page
        self.route = '/'
        username = page.session.get('username')
        self.controls = [
            ft.AppBar(title=ft.Text(f"Jury System, user: {username}"), bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST),
            ft.ElevatedButton("Users", on_click=lambda _: self.page.go("/users")),
            ft.ElevatedButton("Athletes", on_click=lambda _: self.page.go("/athletes")),
            ft.ElevatedButton("Settings", on_click=lambda _: self.page.go("/settings")),
            ft.ElevatedButton("Logout", on_click=self.logout),
        ]

    def logout(self, e):
        self.page.session.clear()
        self.page.go('/login')

    def did_mount(self):
        print('Did mount')
        self.update()

    def will_unmount(self):
        print('Will unmount')
        
class LoginView(ft.View):
    def __init__(self, page: ft.Page):
        super().__init__()
        self.page = page
        self.route = '/login'
        db = JuryDatabase('db')

        def loginbtn(e):
            userId = db.validateUser(username.value, password.value)
            if userId is not None:
                print("Redirecting...")
                self.page.session.set('userId', userId)
                self.page.session.set('username', username.value)
                self.page.go('/home')
            else:
                print("Login failed !!!")
                self.page.open(ft.SnackBar(
                    ft.Text("wrong login, user expired or locked", size=30),
                    bgcolor="red"
                ))
        username = ft.TextField(label="User name")
        password = ft.TextField(label="Password", password=True, can_reveal_password=True, on_submit=loginbtn)
    
        self.controls = [username, password,ft.ElevatedButton("Login Now",
                                  bgcolor="blue", color="white",
                                  on_click=loginbtn)]
        
    def did_mount(self):
        print('Did mount')
        self.update()

    def will_unmount(self):
        print('Will unmount')


