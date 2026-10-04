from django.shortcuts import render, redirect
from .models import Flight, Booking

def home(request):
    flights = Flight.objects.all()
    return render(request, "home.html", {"flights": flights})


def search_flights(request):
    departure = request.GET.get("from")
    arrival = request.GET.get("to")
    date = request.GET.get("date")

    flights = Flight.objects.all()

    if departure:
        flights = flights.filter(departure__icontains=departure)

    if arrival:
        flights = flights.filter(arrival__icontains=arrival)

    if date:
        flights = flights.filter(date=date)

    return render(request, "home.html", {
    "flights": flights,
    "departure": departure,
    "arrival": arrival,
    "date": date
})


def book_flight(request, flight_id):
    flight = Flight.objects.get(id=flight_id)

    if request.method == "POST":
        passenger_name = request.POST.get("passenger_name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        seats = request.POST.get("seats")

        Booking.objects.create(
            flight=flight,
            passenger_name=passenger_name,
            email=email,
            phone=phone,
            seats=seats
        )

        return redirect("booking_success", flight_id=flight.id)

    return render(request, "booking.html", {"flight": flight})


def booking_success(request, flight_id):
    flight = Flight.objects.get(id=flight_id)
    booking = Booking.objects.filter(flight=flight).last()

    return render(request, "booking_success.html", {
        "flight": flight,
        "booking": booking
    })
# Create your views here.
