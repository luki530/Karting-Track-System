from django.db import models


class Client(models.Model):
    name = models.CharField(max_length=45)
    email = models.CharField(max_length=45)        
    client_number = models.CharField(max_length=45)
    sex = models.CharField(max_length=1)

    class Meta:
        db_table = 'client'


class Kart(models.Model):
    kart_number = models.IntegerField(unique=True)
    kart_model = models.ForeignKey('KartModel', models.DO_NOTHING)

    class Meta:
        db_table = 'kart'


class KartModel(models.Model):
    name = models.CharField(max_length=45)
    power = models.IntegerField()
    number_of_seats = models.IntegerField()

    class Meta:
        db_table = 'kart_model'


class Lap(models.Model):
    track = models.ForeignKey('Track', models.DO_NOTHING)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField(blank=True, null=True)
    race_drivers = models.ForeignKey('RaceDrivers', models.DO_NOTHING)

    class Meta:
        db_table = 'lap'


class Race(models.Model):
    date = models.DateField()
    number = models.IntegerField()

    class Meta:
        db_table = 'race'


class RaceDrivers(models.Model):
    race = models.OneToOneField(Race, models.DO_NOTHING)
    kart = models.OneToOneField(Kart, models.DO_NOTHING)
    client = models.OneToOneField(Client, models.DO_NOTHING)

    class Meta:
        db_table = 'race_drivers'


class Track(models.Model):
    name = models.CharField(max_length=45)

    class Meta:
        db_table = 'track'
