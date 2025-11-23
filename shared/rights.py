import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "."))
from database import *

@dataclass
class Route():
    _name: str
    _route: str
    _allowed: list[Restrictions]

    def route(self, **kwargs) -> str:
        for v in kwargs.values():
            if v is None:
                return None
        try:
            return self._route.format(**kwargs)
        except KeyError:
            pass
        return None
    
    def name(self):
        return self._name
    
    def isAllowed(self, user: User) -> bool:
        for allowed in self._allowed:
            if user.restrictions.value == allowed.value:
                return True
        return False


routes = [
    Route("Users", "/users", [Restrictions.ADMIN]),
    Route("Athletes", "/athletes", [Restrictions.TRAINER]),
    Route("Attendances", "/attendances", [Restrictions.HOST, Restrictions.TRAINER]),
    Route("Events", "/events", [Restrictions.HOST, Restrictions.TRAINER]),
    Route("Rating", "/rating/{eventId}", [Restrictions.HOST, Restrictions.JUDGE]),
    Route("Ranking", "/ranking/{eventId}", [Restrictions.HOST]),
    Route("Settings", "/settings", Restrictions)
]

def allowedRoutes(user: User) -> list[Route]:
    ret = []
    if not user:
        return ret
    for route in routes:
        if route.isAllowed(user):
            ret.append(route)
    return ret