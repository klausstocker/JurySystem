import os
import sys
from typing import List
import flet as ft
from view import View
import datetime

sys.path.append(os.path.join(os.path.dirname(__file__), "../.."))
from shared.database import Gender, RankingType, EventCategory


class CategoriesView(View):
    def __init__(self, page: ft.Page, db, redis, eventId: int):
        super().__init__(page, db, redis)
        self.route = f"/categories/{eventId}"
        self.eventId = eventId
        self.existing_categories: List[EventCategory] = []

        # ======== INTERN gespeicherte Werte ========
        self.birth_from = None
        self.birth_to = None
        self.editing_old_name = None
        self.editing_algo = None

        # ======== Eingabefelder ========

        name_field = ft.TextField(label="Category Name", width=350)

        gender_field = ft.Dropdown(
            label="Gender",
            width=200,
            options=[ft.dropdown.Option(g.name) for g in Gender]
        )

        ranking_type_field = ft.Dropdown(
            label="Ranking Type",
            width=200,
            options=[ft.dropdown.Option(r.name) for r in RankingType]
        )

        # ========= Geburtsdatum Textfelder (jetzt 240px breit!) =========
        birth_from_text = ft.TextField(label="Birth From", read_only=True, width=240)
        birth_to_text = ft.TextField(label="Birth To", read_only=True, width=240)

        # ========= DatePicker Functions =========

        def set_birth_from(e):
            if e.data:
                self.birth_from = datetime.datetime.fromisoformat(e.data)
                birth_from_text.value = e.data
                page.update()

        def set_birth_to(e):
            if e.data:
                self.birth_to = datetime.datetime.fromisoformat(e.data)
                birth_to_text.value = e.data
                page.update()

        picker_from = ft.DatePicker(
            on_change=set_birth_from,
            first_date=datetime.datetime(1980, 1, 1),
            last_date=datetime.datetime(2030, 12, 31)
        )

        picker_to = ft.DatePicker(
            on_change=set_birth_to,
            first_date=datetime.datetime(1980, 1, 1),
            last_date=datetime.datetime(2030, 12, 31)
        )

        # ========= Buttons zum Öffnen der DatePicker =========

        birth_from_button = ft.IconButton(
            icon=ft.Icons.CALENDAR_MONTH,
            tooltip="Pick date",
            on_click=lambda _: page.open(picker_from)
        )

        birth_to_button = ft.IconButton(
            icon=ft.Icons.CALENDAR_MONTH,
            tooltip="Pick date",
            on_click=lambda _: page.open(picker_to)
        )

        # ========= SAVE BUTTON =========
        def save_clicked(e):
            try:
                algo = self.editing_algo if self.editing_algo else EventCategory.defaultRankingAlgo()
                cat = EventCategory(
                    name_field.value,
                    self.eventId,
                    Gender[gender_field.value],
                    self.birth_from,
                    self.birth_to,
                    RankingType[ranking_type_field.value],
                    algo
                )

                success = False
                if self.editing_old_name:
                    if self.db.updateEventCategory(cat, self.editing_old_name):
                        page.open(ft.SnackBar(ft.Text("Category updated", size=18), bgcolor="green"))
                        success = True
                    else:
                        page.open(ft.SnackBar(ft.Text("Error updating category", size=18), bgcolor="red"))
                else:
                    if self.db.insertEventCategory(cat):
                        page.open(ft.SnackBar(ft.Text("Category saved", size=18), bgcolor="green"))
                        success = True
                    else:
                        page.open(ft.SnackBar(ft.Text("Error saving category", size=18), bgcolor="red"))

                if success:
                    # Clear input fields
                    name_field.value = ""
                    gender_field.value = None
                    birth_from_text.value = ""
                    birth_to_text.value = ""
                    self.birth_from = None
                    self.birth_to = None
                    ranking_type_field.value = None
                    self.editing_old_name = None
                    self.editing_algo = None

                    # Refresh the view to show the new category
                    self.table.rows = create_rows()
                    self.table.update()
                    self.page.update()

            except Exception as ex:
                page.open(ft.SnackBar(ft.Text(f"Error: {ex}", size=18), bgcolor="red"))

        save_button = ft.IconButton(
            icon=ft.Icons.CHECK_CIRCLE,
            icon_color=ft.Colors.GREEN_400,
            tooltip="Save",
            on_click=save_clicked
        )

        # ========= Input controls for new categories =========
        input_controls = ft.Row(
            controls=[
                name_field,
                gender_field,
                ft.Row(controls=[birth_from_text, birth_from_button]),
                ft.Row(controls=[birth_to_text, birth_to_button]),
                ranking_type_field,
                save_button,
            ],
            alignment=ft.MainAxisAlignment.SPACE_AROUND,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        )

        def edit_clicked(e, category: EventCategory):
            name_field.value = category.name
            gender_field.value = category.gender.name
            self.birth_from = category.birthFrom
            self.birth_to = category.birthTo
            birth_from_text.value = str(category.birthFrom) if category.birthFrom else ""
            birth_to_text.value = str(category.birthTo) if category.birthTo else ""
            ranking_type_field.value = category.rankingType.name
            
            self.editing_old_name = category.name
            self.editing_algo = category.rankingAlgo
            page.update()

        def delete_clicked(e, category_name):
            def confirm_delete(e):
                if self.db.removeEventCategory(self.eventId, category_name):
                    page.open(ft.SnackBar(ft.Text("Category deleted", size=18), bgcolor="green"))
                    self.table.rows = create_rows()
                    self.table.update()
                else:
                    page.open(ft.SnackBar(ft.Text("Error deleting category", size=18), bgcolor="red"))
                page.close(dlg)

            dlg = ft.AlertDialog(
                modal=True,
                title=ft.Text("Confirm Deletion"),
                content=ft.Text(f"Do you want to delete the category '{category_name}'?"),
                actions=[
                    ft.TextButton("Yes", on_click=confirm_delete),
                    ft.TextButton("No", on_click=lambda e: page.close(dlg)),
                ],
                actions_alignment=ft.MainAxisAlignment.END,
            )
            page.open(dlg)

        # ========= Load existing categories and create rows for them =========
        def create_rows():
            rows = []
            for cat in self.db.getEventCategories(self.eventId):
                rows.append(
                    ft.DataRow(
                        cells=[
                            ft.DataCell(ft.Text(cat.name)),
                            ft.DataCell(ft.Text(cat.gender.name)),
                            ft.DataCell(ft.Text(cat.birthFrom.strftime('%Y-%m-%d') if cat.birthFrom else "")),
                            ft.DataCell(ft.Text(cat.birthTo.strftime('%Y-%m-%d') if cat.birthTo else "")),
                            ft.DataCell(ft.Text(cat.rankingType.name)),
                            ft.DataCell(ft.Row([
                                ft.IconButton(icon=ft.Icons.EDIT, icon_color=ft.Colors.BLUE, on_click=lambda e, c=cat: edit_clicked(e, c)),
                                ft.IconButton(icon=ft.Icons.DELETE, icon_color=ft.Colors.RED, on_click=lambda e, n=cat.name: delete_clicked(e, n))
                            ]))
                        ]
                    )
                )
            return rows

        # ========== Tabelle (GUI Layout) ==========

        self.table = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("Name")),
                ft.DataColumn(ft.Text("Gender")),
                ft.DataColumn(ft.Text("Birth From")),
                ft.DataColumn(ft.Text("Birth To")),
                ft.DataColumn(ft.Text("Ranking Type")),
                ft.DataColumn(ft.Text("Actions")),
            ],
            rows=create_rows()
        )

        self.controls = [
            ft.AppBar(
                title=ft.Text("Categories"),
                bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST
            ),
            ft.Text("Add new Category", size=20),
            input_controls,
            self.table,
            ft.ElevatedButton("Back", on_click=lambda _: self.page.go("/events"))
        ]

        # Add pickers to the page's overlay so they can be opened from anywhere
        page.overlay.extend([picker_from, picker_to])
        # No need to call page.update() here as the view will be built and updated by the navigator
