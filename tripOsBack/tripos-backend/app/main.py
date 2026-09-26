from fastapi import FastAPI

from app.routes import (
    accommodations,
    admin,
    ai,
    auth,
    budgets,
    checklists,
    destinations,
    documents,
    expenses,
    itinerary,
    memories,
    notifications,
    packing,
    places,
    reminders,
    saved_places,
    screenshots,
    transports,
    trips,
    users,
    wallet,
)
from app.core.config import settings


app = FastAPI(title=settings.APP_NAME)

for route_module in (
    auth,
    users,
    destinations,
    places,
    saved_places,
    trips,
    itinerary,
    budgets,
    wallet,
    expenses,
    packing,
    checklists,
    accommodations,
    transports,
    documents,
    screenshots,
    reminders,
    notifications,
    memories,
    ai,
    admin,
):
    app.include_router(route_module.router)


@app.get("/health", tags=["health"])
def health_check() -> dict[str, str]:
    return {"status": "ok"}