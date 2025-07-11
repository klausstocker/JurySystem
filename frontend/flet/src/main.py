import flet as ft
from navigation import Navigator

def main(page: ft.Page):
    page.title = "Jury System"
    navi = Navigator(page)
    page.on_route_change = navi.route_change
    page.on_view_pop = navi.view_pop
    page.theme_mode = ft.ThemeMode.DARK
    page.auto_scroll = True
    page.go(page.route)

ft.app(main, assets_dir="assets")

