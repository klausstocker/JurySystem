import os
import sys
from fastapi import FastAPI, Response
from datetime import datetime
from print import printTable

sys.path.append(os.path.join(os.path.dirname(__file__), "../.."))
from shared.database import JuryDatabase, Athlete

api = FastAPI()

@api.get("/test")
async def test():
    return {"message": f"API running {datetime.now()}"}

@api.get('/athletes/{userId}')
async def athletes(userId: int):
    db = JuryDatabase('db')
    data = [[athlete.name(), athlete.birthFormated(), athlete.gender.name] for athlete in db.getAthletes(userId)]
    user = db.getUser(userId)
    data = printTable('Athletes', user.team, '', ['name', 'birth', 'gender'], data )
    headers = {'Content-Disposition': 'attachment; filename="athletes.pdf"'}
    return Response(data, headers=headers, media_type='application/pdf')



