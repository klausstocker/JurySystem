import flet as ft
from navigation import Navigator


def main(page: ft.Page):
    navi = Navigator(page)
    page.title = "Example"

    def connect(e=None):
        print(f'page.connect called {e}')

    def close(e=None):
        print(f'On close event {e}')

    def disconnect(e=None):
        print(f'Disconnect event {e}')

    def lc_state(e=None):
        print(f'Lifecycle State changed {e}')

    page.theme_mode = ft.ThemeMode.DARK
    page.auto_scroll = True
    page.on_connect = connect
    page.on_close = close
    page.on_disconnect = disconnect
    page.on_app_lifecycle_state_change = lc_state
    page.on_route_change = navi.route_change
    page.on_view_pop = navi.view_pop
    page.go(page.route)


ft.app(main, assets_dir="assets")

