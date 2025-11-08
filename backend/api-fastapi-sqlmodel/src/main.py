import os
import sys
from fastapi import FastAPI, Response, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML
from pdf_reports import pug_to_html, write_report, ReportWriter
from datetime import datetime

sys.path.append(os.path.join(os.path.dirname(__file__), "../.."))
from shared.database import JuryDatabase, Athlete

api = FastAPI()

api.mount("/static", StaticFiles(directory="static"), name="static")
env = Environment(loader=FileSystemLoader('templates'))

def createResponse(template: str, context: dict, filename: str) -> Response:
    template = env.get_template('table.html')
    rendered_html = template.render(context)
    pdf_file = HTML(string=rendered_html).write_pdf()
    headers = {'Content-Disposition': f'attachment; filename="{filename}"'}
    return Response(pdf_file, headers=headers, media_type='application/pdf')

def alphaNum(text: str) -> str:
    return ''.join(x for x in text if x.isalnum())

@api.get("/test")
async def test():
    return {"message": f"API running {datetime.now()}"}

@api.get('/athletes/{userId}', response_class=HTMLResponse)
async def athletes(userId: int):
    db = JuryDatabase('db')
    data = [[athlete.name(), athlete.birthFormated(), athlete.gender.name] for athlete in db.getAthletes(userId)]
    user = db.getUser(userId)

    context = {
            "title": f'Athletes of {user.team}',
            "headers": ['name', 'birth', 'gender'],
            "data": data
        }
    return createResponse('table.html', context, f'athletes_{alphaNum(user.team)}.pdf')

@api.get('/attendances/{userId}/{eventId}', response_class=HTMLResponse)
async def attendances(userId: int, eventId: int):
    db = JuryDatabase('db')
    event = db.getEvent(eventId)
    athleteAttendances = []
    for attendance in db.getAttendances(eventId, userId):
        athleteAttendances.append((attendance, db.getAthlete(attendance.athleteId)))

    data = [[a.name(), a.birthFormated(), a.gender.name, b.eventCategoryName, b.group] for b, a in athleteAttendances]
    print(data)
    user = db.getUser(userId)

    context = {
            "title": f'Attendances for {event.descr()} of {user.team}',
            "headers": ['name', 'birth', 'gender', 'category', 'group'],
            "data": data
        }
    return createResponse('table.html', context, f'attendance_{alphaNum(event.name)}_{alphaNum(user.team)}.pdf')

@api.get('/certificate/{eventId}/{athleteId}', response_class=HTMLResponse)
async def certificate(eventId: int, athleteId: int):
    db = JuryDatabase('db')
    event = db.getEvent(eventId)
    athlete = db.getAthlete(athleteId)
    attendance = db.getAttendance(athleteId, eventId)
    html = pug_to_html("templates/certificate.pug", title=f'{athlete.name()} - {event.name}', event=event, athlete=athlete, attendance=attendance)
    pdf = write_report(html, base_url='static')
    filename = f'{alphaNum(athlete.name())}_{alphaNum(event.name)}.pdf'
    headers = {'Content-Disposition': f'attachment; filename="{filename}"'}
    return Response(pdf, headers=headers, media_type='application/pdf')




