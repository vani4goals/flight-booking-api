from fastapi import FastAPI
from app.routes import flights, bookings

app = FastAPI(
    title="Flight Booking API",
    description="A sample API for searching and booking flights",
    version="1.0.0",
)

app.include_router(flights.router, prefix="/flights", tags=["Flights"])
app.include_router(bookings.router, prefix="/bookings", tags=["Bookings"])


@app.get("/")
def root():
    return {"message": "Welcome to the Flight Booking API"}
