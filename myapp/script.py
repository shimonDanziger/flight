import os
import sys
import django
import csv
import random
import time
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "flight.settings")
django.setup()
from myapp.models import Flight
import psutil

def is_computer_stressed(cpu_threshold=80, memory_threshold=80):
    """
    Checks CPU and memory usage to gauge potential computer stress.

    Args:
        cpu_threshold (int, optional): CPU usage percentage threshold (default: 80).
        memory_threshold (int, optional): Memory usage percentage threshold (default: 80).

    Returns:
        bool: True if CPU or memory usage exceeds thresholds, False otherwise.
    """
    cpu_usage = psutil.cpu_percent()
    memory_usage = psutil.virtual_memory().percent
   

    return cpu_usage > cpu_threshold or memory_usage > memory_threshold

# # Example usage
# if is_computer_stressed():
#     print("Your computer seems stressed! Consider optimizing code or chunking data.")
# else:
#     print("Computer resources appear available for data analysis.")

# # ... your data analysis code here ...


def import_flights(file_path):
    with open(file_path, 'r') as file:
        reader = csv.DictReader(file)
        

        for row in reader:
            while is_computer_stressed():
                time.sleep(0)
            s = random.randint(1, 10)
            i = random.randint(1, 10)
            if i ==  s:
                try:
                    
                    if row['isNonStop'] == 'True':
                        segmentsArrivalAirportCode1 = row['segmentsArrivalAirportCode']
                        segmentsDepartureAirportCode1 = row['segmentsDepartureAirportCode']
                        segmentsAirlineName1 = row['segmentsAirlineName']
                        segmentsArrivalTimeEpochSeconds1 = int(row['segmentsArrivalTimeEpochSeconds'])
                        segmentsDepartureTimeEpochSeconds1 = int(row['segmentsDepartureTimeEpochSeconds'])
                    else:
                        segmentsArrivalAirportCode1 = row['segmentsArrivalAirportCode'].split('||')[1]
                        segmentsDepartureAirportCode1 = row['segmentsDepartureAirportCode'].split('||')[1]
                        segmentsAirlineName1 = row['segmentsAirlineName'].split('||')[1]
                        segmentsArrivalTimeEpochSeconds1 = int(row['segmentsArrivalTimeEpochSeconds'].split('||')[1])
                        segmentsDepartureTimeEpochSeconds1 = int(row['segmentsDepartureTimeEpochSeconds'].split('||')[0])
                        
                    # Ensure totalFare is handled correctly, convert to Decimal if necessary
                    total_fare = row['totalFare']
                    if total_fare == 'UNKNOWN':
                        total_fare = 0  # or set a default value
                    else:
                        total_fare = float(total_fare)  # or handle conversion as needed
                    Flight.objects.create(
                        legId = row['legId'],
                        destinationAirport = row['destinationAirport'],
                        totalFare = total_fare,
                        segmentsArrivalTimeEpochSeconds = segmentsArrivalTimeEpochSeconds1,
                        segmentsDepartureTimeEpochSeconds = segmentsDepartureTimeEpochSeconds1,
                        segmentsArrivalAirportCode = segmentsArrivalAirportCode1,
                        segmentsDepartureAirportCode = segmentsDepartureAirportCode1,
                        segmentsAirlineName = segmentsAirlineName1,
                    )
                   
                    
                    #print(f"Successfully imported flight: {segmentsAirlineName1} from {segmentsDepartureAirportCode1} to {segmentsArrivalAirportCode1}")
                except Exception as e:
                    print(f"Error creating Flight object: {e}")
                    



csv_file_path = r"C:\Users\99888\Flight\db\itineraries.csv"
import_flights(csv_file_path)
    
    # distinct_airports = Flight.objects.values('destination').distinct()
    # total_flights = 0
    # for each in distinct_airports:
    #     fl = origen(each['destination'])
    #     total_flights += len(fl)
          
    # print(total_flights)

   
