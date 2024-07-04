import os
import sys
import django
from django.db.models import Min
import random
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "flight.settings")
django.setup()
from myapp.models import Flight

def find_flights(origin, origin_key, departure_after, max_day_flight):
    """
    Filters flights based on origin, departure time, and max duration.

    Args:
        origin: The departure airport code (string).
        departure_after: A timestamp in seconds since epoch (integer).
        max_day_flight: Maximum allowed flight duration in days (integer).

    Returns:
        A queryset of flights matching the criteria.
    """
    flights = Flight.objects.filter(
        segmentsDepartureAirportCode=origin,
        segmentsDepartureTimeEpochSeconds__gt=departure_after,
        segmentsArrivalTimeEpochSeconds__lt=max_day_flight
    )
    

   
          

    return flights




def check_flight(flight_id,flight_place,place):
        if flight_id[place]== 0:
            return
        check_flight(flight_id,flight_place,flight_place[place])
        cheap_flight = Flight.objects.all().filter(legId=flight_id[place]).first()
        print(cheap_flight)
        
        return



def engine(origin, destination, departure_after, max_day_flight, max_stop):
    price = 0
    max_day_flight += departure_after + max_day_flight * 86400
    
    new_flights = find_flights(origin, '', departure_after, max_day_flight)
    flight_list =[]
    flight_list_price =[0.0]
    flight_id =[0]
    flight_place =[-1]
    flight_list.append(new_flights)
    

    i = 0
    cheap_flight_place = 0

    
    
    cheap_flight = flight_list[0].order_by('totalFare').first()
    
    
   
    cheap_flight_place = 0
    try:
        while cheap_flight.segmentsArrivalAirportCode != destination and i < 1000:
            
            cheap_flight_place_old = cheap_flight_place
            new_flights = find_flights(
                cheap_flight.segmentsArrivalAirportCode,
                cheap_flight.legId,
                cheap_flight.segmentsArrivalTimeEpochSeconds,
                max_day_flight
            )
            print(new_flights.all().count())
            flight_list.append(new_flights)
            
            i += 1
            flight_list_price.append(float(cheap_flight.totalFare) + flight_list_price[cheap_flight_place])
            #flight_id.append(cheap_flight.legId)
            #flight_place.append(cheap_flight_place)
            cheap_price = float('inf')
            
            
            for j, flight_queryset in enumerate(flight_list):
                if flight_queryset.exists():
                    min_total_fare = flight_queryset.aggregate(Min('totalFare'))['totalFare__min']

                        # Get the first flight with the minimum totalFare
                    first_flight = flight_queryset.filter(totalFare=min_total_fare).first()
                    
                    if first_flight.totalFare < cheap_price:
                        cheap_flight = first_flight
                        cheap_price = first_flight.totalFare
                        cheap_flight_place = j
                        # Remove the flight from the queryset
                        flight_list[j] = flight_queryset.exclude(legId=cheap_flight.legId)
            
            if cheap_flight:
                cheap_flight_destination = cheap_flight.segmentsArrivalAirportCode
               
            else:
                break  # No more flights found
            
    except Exception as e:
        print(f"Error: {e}")

       
    if cheap_flight:
        print(float(cheap_flight.totalFare) + flight_list_price[cheap_flight_place]) 
    
           

    
        # print(flight_id)
        # print(flight_place)
        # print(cheap_flight_place_old)
        check_flight(flight_id,flight_place,cheap_flight_place_old+1)
        print(cheap_flight) 


    return flight_list



distinct_departure_airports = Flight.objects.values_list('segmentsDepartureAirportCode', flat=True).distinct()

# Convert the queryset to a list (optional)
distinct_departure_airport_list = list(distinct_departure_airports)
print(len(distinct_departure_airport_list))

engine(distinct_departure_airport_list[int(random.randint(0, 115))], distinct_departure_airport_list[int(random.randint(0, 115))], 1650895080, 3, 0)

