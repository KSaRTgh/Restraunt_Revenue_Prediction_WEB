from django.contrib.auth.models import User
from django.core.validators import *
from django.db import models


class Data(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    City = models.IntegerField(blank=False)
    Month = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(12)], blank=False)
    Year = models.IntegerField(validators=[MinValueValidator(1000), MaxValueValidator(2400)], blank=False)
    City_Group_BigCities = models.BooleanField(default=False)
    City_Group_Other = models.BooleanField(default=False)
    Type_DT	 = models.BooleanField(default=False)
    Type_FC = models.BooleanField(default=False)
    Type_IL = models.BooleanField(default=False)
    P2 = models.FloatField(blank=False)
    P6 = models.FloatField(blank=False)
    P28 = models.FloatField(blank=False)
    P27 = models.FloatField(blank=False)
    P22 = models.FloatField(blank=False)
    P23 = models.FloatField(blank=False)
    #is_preprocessed = models.BooleanField(default=False)
    prediction = models.FloatField(default=None, null=True)

    def __str__(self):
        return str(self.pk)