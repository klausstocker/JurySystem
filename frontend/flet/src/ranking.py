import os
import sys
import flet as ft
from view import View

sys.path.append(os.path.join(os.path.dirname(__file__), "../.."))
from shared.database import JuryDatabase, Athlete, AthleteRatings, AthleteRanking, Gender

def ratingCell(ratings: AthleteRatings, discipline: str):
    if discipline not in ratings.ratings.keys():
        return ft.DataCell(ft.Text('---'))
    difficulty, execution = ratings.ratings[discipline].pretty()
    return ft.DataCell(ft.Row(spacing=5, controls=[ft.Text(difficulty), ft.Text(execution)]))
    
class RankingView(View):
    def __init__(self, page: ft.Page, eventId: int):
        super().__init__(page)
        self.route = f'/ranking/{eventId}'

        self.user = self.page.session.get('user')
        self.event = self.db.getEvent(eventId)
        self.disciplines = self.db.getEventDisciplines(eventId)
        self.categories = self.db.getEventCategories(eventId)
        self.rankings = []
        
        def updateRankings(e):
            self.rankings = self.db.getEventCategoryRankings(self.event.id, self.categoryEdit.value)
            self.updateControls()

        self.categoryEdit = ft.Dropdown(
            label="Category",
            width = 300,
            options=[ft.dropdownm2.Option(d.name) for d in self.categories],
            on_change=updateRankings
        )

        self.updateControls()

    def AthleteRankingAsRow(self, ranking: AthleteRanking):
        cells = [
            ft.DataCell(ft.Text(ranking.ranking)),
            ft.DataCell(ft.Text(ranking.ratings.athlete.name()))
            ]
        cells += [ratingCell(ranking.ratings, d.name) for d in self.disciplines]
        cells.append(ft.DataCell(ft.Text('{:.2f}'.format(ranking.ratings.sum()))))
        return ft.DataRow(cells=cells)
        
    def updateControls(self):
        self.table = ft.DataTable(
                columns=[ft.DataColumn(ft.Text(h)) for h in ['rank', 'name'] + [d.name for d in self.disciplines] + ['sum']],
                rows= [self.AthleteRankingAsRow(ranking) for ranking in self.rankings]
            )

        self.controls = [
            ft.AppBar(title=ft.Text('Ranking'), bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST),
            ft.Text(self.event.name, size=30, color=ft.Colors.PINK_600, italic=True),
            self.categoryEdit,
            self.table,
            ft.ElevatedButton("Home", on_click=lambda _: self.page.go("/"))]
        self.page.update()


