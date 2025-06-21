from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect
from .models import *

# Create your views here.
def index(request):
    return render(request, "flights/index.html", {
        "flights": Flight.objects.all(),
    })


def flight(request, flight_id):
    # get the flight which id=flight_id
    flight = Flight.objects.get(id=flight_id)
    # passengers belong to each flight, could be None
    passengers = flight.passengers.all()
    non_passengers = [p for p in Passenger.objects.all() if p not in passengers]

    return render(request, "flights/flight.html", {
        "flight_id": flight_id,
        "flight": flight,
        "passengers": passengers,
        "non_passengers": non_passengers,
    })


def book(request, flight_id):
    flight = Flight.objects.get(id=flight_id)
    # passengers already booked/tooked this flight
    passengers = flight.passengers.all()
    # passengers that are not on this flight
    non_passengers = [p for p in Passenger.objects.all() if p not in passengers]

    # handle post request
    if request.method == "POST":
        passenger_id = request.POST.get("passenger") # "passenger" is the name of the html form
        # if this is not None, means this is an available passenger (Not none)
        if passenger_id:
            try:
                passenger = Passenger.objects.get(id=int(passenger_id))
                # if passenger is not on this flight (means he is allowed for booking this flight)
                if passenger in non_passengers:  
                    # book this flight for the passenger
                    passenger.flights.add(flight)
                    return HttpResponseRedirect(reverse("flight", args=(flight.id,)))
            except Passenger.DoesNotExist:
                pass
        else:
            # rerender the booking page as this is not a valid passenger (might be on the flight already)
            return render(request, "flights/flight.html", {
                "flight_id": flight_id,
                "flight": flight,
                "passengers": passengers,
                "non_passengers": non_passengers,
            })


    # handle get request
    return render(request, "flights/flight.html", {
        "flight_id": flight_id,
        "flight": flight,
        "passengers": passengers,
        "non_passengers": non_passengers,
    })