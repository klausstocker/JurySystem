import os
import sys
from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select
from db import get_session, init_db
from models import User
from datetime import datetime

try:
    from shared.foo import module
except ImportError:
    # need to append paths
    sys.path.append(os.path.join(os.path.dirname(__file__), "../.."))
    sys.path.append(os.path.join(os.path.dirname(__file__), "../../.."))
    from shared.foo import module
api = FastAPI()


@api.get("/test")
async def test():
    return {"message": f"API running {datetime.now()}"}


@api.get("/users", response_model=list[User])
async def get_users(session: AsyncSession = Depends(get_session),
                    user_id: int = 0):
    if user_id == 0:
        return await session.exec(select(User).order_by(User.id))
    elif user_id >= 1:
        return await session.exec(select(User).where(User.id == user_id).order_by(User.id))
    else:
        return list()
