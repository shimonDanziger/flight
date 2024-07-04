from django.db import models



class Flight(models.Model):
    legId = models.CharField(max_length=100, primary_key=True)
    legIdBack = models.CharField(max_length=100,default='UNKNOWN')
    destinationAirport = models.CharField(max_length=100)
    totalFare = models.DecimalField(max_digits=10, decimal_places=2)

    segmentsArrivalTimeEpochSeconds = models.IntegerField()
    segmentsDepartureTimeEpochSeconds = models.IntegerField()
    segmentsArrivalAirportCode = models.CharField(max_length=100)
    segmentsDepartureAirportCode = models.CharField(max_length=100)
    segmentsAirlineName = models.CharField(max_length=100)



    def __str__(self):
        return f"Flight {self.legId}: {self.segmentsDepartureAirportCode} to {self.segmentsArrivalAirportCode} cost {self.totalFare}"
