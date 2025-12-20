import flet as ft
from navigation import Navigator

def main(page: ft.Page):
    page.title = "Jury System"
    navi = Navigator(page)
    page.on_route_change = navi.route_change
    page.on_view_pop = navi.view_pop
    page.theme_mode = ft.ThemeMode.DARK
    page.scroll = ft.ScrollMode.AUTO
    page.go(page.route)

ft.app(target=main, view=ft.AppView.WEB_BROWSER, assets_dir="assets")
