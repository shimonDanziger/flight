import os
import sys
import django
import csv

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "flight.settings")
django.setup()

from myapp.models import Flight

def import_flights(file_path):
    with open(file_path, 'r') as file:
        reader = csv.DictReader(file)
        
        for row in reader:
            try:
                Flight.objects.create(
                    airline=row['Airline'],
                    source=row['Source'],
                    destination=row['Destination'],
                    total_stops=int(row['Total_Stops']),
                    price=int(row['Price']),
                    date=int(row['Date']),
                    month=int(row['Month']),
                    year=int(row['Year']),
                    dep_hours=int(row['Dep_hours']),
                    dep_min=int(row['Dep_min']),
                    arrival_hours=int(row['Arrival_hours']),
                    arrival_min=int(row['Arrival_min']),
                    duration_hours=int(row['Duration_hours']),
                    duration_min=int(row['Duration_min'])
                )
                print(f"Successfully imported flight: {row['Airline']} from {row['Source']} to {row['Destination']}")
            except Exception as e:
                print(f"Error creating Flight object: {e}")

if __name__ == '__main__':
    csv_file_path = r"C:\Users\99888\Flight\db\flight_dataset.csv"
    import_flights(csv_file_path)