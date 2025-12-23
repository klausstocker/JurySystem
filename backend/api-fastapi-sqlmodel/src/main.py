import io
import os
import sys
from fastapi import FastAPI, Response, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML
from datetime import datetime
import qrcode
from redis import StrictRedis

sys.path.append(os.path.join(os.path.dirname(__file__), "../.."))
from shared.database import JuryDatabase, Athlete

r = StrictRedis(host='redis', port=6379, db=0, password='redispass', decode_responses=True)

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

@api.get('/ranking/{eventId}/{category}', response_class=HTMLResponse)
async def ranking(eventId: int, category: str):
    db = JuryDatabase('db')
    event = db.getEvent(eventId)
    disciplines = db.getEventDisciplines(eventId)
    data = []
    for rank in db.getEventCategoryRankings(eventId, category):
        athlete = rank.ratings.athlete
        ratingData = []
        for discipline in disciplines:
            ratingData.append(rank.ratings.prettyOrDefault(discipline.name))
        user = db.getUser(athlete.userId)
        data.append([rank.ranking, athlete.name(), user.team] + ratingData + [rank.ratings.sum()])

    context = {
            "title": f'Rankings for {event.descr()} / {category}',
            "headers": ['rank', 'name', 'team'] + [d.name for d in disciplines] + ['rating'],
            "data": data
        }
    return createResponse('table.html', context, f'ranking_{category}.pdf')


@api.get('/certificate/{eventId}', response_class=HTMLResponse)
async def certificate(eventId: int):
    db = JuryDatabase('db')
    event = db.getEvent(eventId)
    athleteAttendances = []
    for attendance in db.getEventAttendances(eventId):
        athleteAttendances.append((attendance, db.getAthlete(attendance.athleteId)))

    template = env.get_template('certificate.html')
    context = {
        "title": f'{event.name}',
        "event": event,
        "athleteAttendances": athleteAttendances
    }
    rendered_html = template.render(context)
    pdf_file = HTML(string=rendered_html, base_url=".").write_pdf()
    filename = f'{alphaNum(event.name)}.pdf'
    headers = {'Content-Disposition': f'attachment; filename="{filename}"'}
    return Response(pdf_file, headers=headers, media_type='application/pdf')


def get_bytes(image):
    img_byte_arr = io.BytesIO()
    image.save(img_byte_arr, format='png')
    return img_byte_arr.getvalue()

@api.get('/qrcodes/login/{token}/{userId}', response_class=HTMLResponse)
async def qrCodesLogin(userId: int, token: str, request: Request) ->Response:
    if r.get(token) is None:
        raise HTTPException(
            status_code=401,
            detail="unautohrized"
        )
    db = JuryDatabase('db')
    user = db.getUser(userId)
    if user is None:
        raise HTTPException(
            status_code=404,
            detail="user not found"
        )
    img = qrcode.make(f'https://{os.environ['SUBDOMAIN_FLET'] + os.environ['DOMAIN']}/autoLogin/{user.username}/{user.token}')
    filename = f'login_{alphaNum(user.username)}.png'
    headers = {'Content-Disposition': f'attachment; filename="{filename}"'}
    return Response(get_bytes(img), headers=headers, media_type='application/png')

