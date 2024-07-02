from django.db import models



class Flight(models.Model):
    legId = models.CharField(max_length=100, primary_key=True)
    destinationAirport = models.CharField(max_length=100)
    totalFare = models.DecimalField(max_digits=10, decimal_places=2)
    segmentsArrivalTimeEpochSeconds = models.IntegerField()
    segmentsDepartureTimeEpochSeconds = models.IntegerField()
    segmentsArrivalAirportCode = models.CharField(max_length=100)
    segmentsDepartureAirportCode = models.CharField(max_length=100)
    segmentsAirlineName = models.CharField(max_length=100)
    