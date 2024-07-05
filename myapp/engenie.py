import os
import sys
import django
from django.db.models import Min
import random
import time
from django.db.models import Avg

from statistics import mean ,pstdev

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "flight.settings")
django.setup()
from myapp.models import Flight


def find_path(flight, origin,flight_list,cost):
    
    
    

    if flight.segmentsDepartureAirportCode == origin:
        print(f"cost :{cost + flight.totalFare}")
        print(flight)
        return 
    
    cost += flight.totalFare
    for flights in flight_list:
        if flights.legId ==  flight.legIdBack:
            new_flight = flights
    find_path(new_flight,origin,flight_list,cost)

    
    print(flight)
    return 


def find_flights(origin,destamation, departure_after, max_day_flight,legIdBack,maxFlightBack,max_stop):
    if maxFlightBack+1 ==  max_stop:
        flights = Flight.objects.filter(
        segmentsDepartureAirportCode=origin,
        segmentsArrivalAirportCode= destamation,
        segmentsDepartureTimeEpochSeconds__gt=departure_after,
        segmentsArrivalTimeEpochSeconds__lt=departure_after + max_day_flight * 86400
    )
    else: 
        flights = Flight.objects.filter(
        segmentsDepartureAirportCode=origin,
        segmentsDepartureTimeEpochSeconds__gt=departure_after,
        segmentsArrivalTimeEpochSeconds__lt=departure_after + max_day_flight * 86400
    )
    if legIdBack != 0:
        for flight in flights:
            flight.legIdBack =legIdBack
            flight.maxFlightBack = maxFlightBack+1

    

    if legIdBack == 0 and flights.exists()== False:    
        return None 





    return list(flights)

# def check_flight(flight_id, flight_place, place):
#     if flight_id[place] == 0:
#         return
#     check_flight(flight_id, flight_place, flight_place[place])
#     cheap_flight = Flight.objects.filter(legId=flight_id[place]).first()
#     print(cheap_flight)
#     return

def engine(origin, destination, departure_after, max_day_flight, max_stop):
    price = 0
    
    new_flights = find_flights(origin,destination, departure_after, max_day_flight,0,0,max_stop)
    flight_list = []
    flight_remove_list =[]
    flight_list.extend(new_flights)

    i = 0
    cheap_flight_place = 0

    try:
        t0 = time.time()
        
        while i == 0 or ( i < 10000 and    cheap_flight.segmentsArrivalAirportCode != destination ):
            check_exist = False
            cheap_price = float('inf')  # Initialize with a high value
            cheap_flight = None         # Initialize the variable to store the cheapest flight
            
            cheap_flight_place_old = -1  # Initialize to store the index of the cheapest flight
            
            # Iterate over the flight list to find the cheapest flight
            for index, flight in enumerate(flight_list):
               
                
                if flight.idCheck != True:
                    if flight.totalFare < cheap_price :
                        check_exist = True
                        cheap_flight = flight
                        cheap_flight_place_old = index
            
            if  cheap_flight == None:
                i = 1000000
                break
            if cheap_flight_place_old != -1:  # Ensure a valid index
                flight_list[cheap_flight_place_old].idCheck= True
            
            
            new_flights = find_flights(
                    cheap_flight.segmentsArrivalAirportCode,
                    destination,
                    cheap_flight.segmentsArrivalTimeEpochSeconds,
                    max_day_flight,
                    cheap_flight.legId,
                    cheap_flight.maxFlightBack,
                    max_stop

                )
            # print(cheap_flight.legId )
            # print(cheap_flight.legIdBack )
           
            flight_list.extend(new_flights)

           
            i += 1
        t1 = time.time()
        if i > 100 and cheap_flight:
        #     print(i)
            #print(t1-t0)
            print('',end= '')
    except Exception as e:
        print(f"Error: {e}")
        raise
    if cheap_flight == None:
        print("there is no flight")
    elif(cheap_flight.segmentsArrivalAirportCode == destination):
        print('',end='')
        #find_path(cheap_flight, origin,flight_list,0)
    
    else:
        print("can not find")    
        return -1
    return flight_list






distinct_departure_airports = Flight.objects.values_list('segmentsDepartureAirportCode', flat=True).distinct()
distinct_departure_airport_list = list(distinct_departure_airports)
not_find =0
time_list =[]
for i in range(100):
    a = distinct_departure_airport_list[random.randint(0, len(distinct_departure_airport_list) - 1)]
    b = distinct_departure_airport_list[random.randint(0, len(distinct_departure_airport_list) - 1)]

    #print(a + " " + b)
    num = random.randint(1650058870,1664919670)
    while find_flights(a,b, num, 3,0,-1,10)== None:
        
        num = random.randint(1650058870,1664919670)
        
    flight = find_flights(a,b, num, 3,0,-1,10)
    # print(len(flight))
    # print(a +" " +b)
    # print(f"depart after:{num}")
    t0 = time.time()
    if(engine(a, b, num, 3, 3) == -1):
        not_find+=1
    t1 = time.time()
    time_list.append(t1-t0)
     

print(not_find)
print(mean(time_list) )
print(pstdev(time_list) )


