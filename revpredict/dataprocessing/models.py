from django.contrib.auth.models import User
from django.core.validators import *
from django.db import models

from revpredict import settings


city_groups =[('Big Cities', 'Big Cities'),
              ('Other' , 'Other')]

ttypes = [('DT','DT'),
          ('FC','FC'),
          ('IL','IL')]


class RawData(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    original_id = models.IntegerField(blank=False, default=-1)
    Open_Date = models.CharField(blank=False, max_length=20 ,
                                 validators=[RegexValidator(regex=r'^(0[1-9]|1[012])[/](0[1-9]|[12][0-9]|3[01])[/](19|20)\d\d$',
                                                           message='Date should be in format mm/dd/YYYY'),])
    City = models.CharField(blank=False, max_length=40)
    City_Group = models.CharField(blank=False, max_length=40, choices=city_groups, default='Big Cities')
    Type = models.CharField(blank=False, max_length=40, choices=ttypes, default='FC')
    P1 = models.FloatField(default=0)
    P2 = models.FloatField(default=0)
    P3 = models.FloatField(default=0)
    P4 = models.FloatField(default=0)
    P5 = models.FloatField(default=0)
    P6 = models.FloatField(default=0)
    P7 = models.FloatField(default=0)
    P8 = models.FloatField(default=0)
    P9 = models.FloatField(default=0)
    P10 = models.FloatField(default=0)
    P11 = models.FloatField(default=0)
    P12 = models.FloatField(default=0)
    P13 = models.FloatField(default=0)
    P14 = models.FloatField(default=0)
    P15 = models.FloatField(default=0)
    P16 = models.FloatField(default=0)
    P17 = models.FloatField(default=0)
    P18 = models.FloatField(default=0)
    P19 = models.FloatField(default=0)
    P20 = models.FloatField(default=0)
    P21 = models.FloatField(default=0)
    P22 = models.FloatField(default=0)
    P23 = models.FloatField(default=0)
    P24 = models.FloatField(default=0)
    P25 = models.FloatField(default=0)
    P26 = models.FloatField(default=0)
    P27 = models.FloatField(default=0)
    P28 = models.FloatField(default=0)
    P29 = models.FloatField(default=0)
    P30 = models.FloatField(default=0)
    P31 = models.FloatField(default=0)
    P32 = models.FloatField(default=0)
    P33 = models.FloatField(default=0)
    P34 = models.FloatField(default=0)
    P35 = models.FloatField(default=0)
    P36 = models.FloatField(default=0)
    P37 = models.FloatField(default=0)
    revenue = models.FloatField(default=None, null=True)


class Data(models.Model):
    raw = models.OneToOneField(RawData, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    City = models.IntegerField(blank=False)
    Month = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(12)], blank=False)
    Year = models.IntegerField(validators=[MinValueValidator(1000), MaxValueValidator(2400)], blank=False)
    City_Group_BigCities = models.BooleanField(default=False)
    City_Group_Other = models.BooleanField(default=False)
    Type_DT = models.BooleanField(default=False)
    Type_FC = models.BooleanField(default=False)
    Type_IL = models.BooleanField(default=False)
    P2 = models.FloatField(blank=False)
    P6 = models.FloatField(blank=False)
    P28 = models.FloatField(blank=False)
    P27 = models.FloatField(blank=False)
    P22 = models.FloatField(blank=False)
    P23 = models.FloatField(blank=False)
    # is_preprocessed = models.BooleanField(default=False)
    prediction = models.FloatField(default=None, null=True)

    def __str__(self):
        return str(self.pk)