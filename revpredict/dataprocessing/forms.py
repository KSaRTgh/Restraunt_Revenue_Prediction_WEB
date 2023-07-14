from django import forms
from django.contrib.auth.models import User
from django.http import request
from django.contrib import admin
from .models import *
import django_tables2 as tables


class AddToDbForm(forms.ModelForm):
    Month = forms.IntegerField(min_value=1, max_value=12)
    Year = forms.IntegerField(min_value=1000, max_value=2400)
    class Meta:
        model = Data
        fields = ['user', 'City', 'Month','Year','City_Group_BigCities', 'City_Group_Other','Type_DT','Type_FC',
                  'Type_IL','P2', 'P6', 'P28', 'P27', 'P22','P23']


class db_viewTable(tables.Table):
    selection = tables.CheckBoxColumn(accessor="pk", attrs={"th__input": {"onclick": "toggle(this)"}},
                                      orderable=False)
    class Meta:
        model = Data
        fields = ['user', 'City', 'Month','Year','City_Group_BigCities', 'City_Group_Other','Type_DT','Type_FC',
                  'Type_IL','P2', 'P6', 'P28', 'P27', 'P22','P23']


class predictionsTable(tables.Table):
    class Meta:
        model = Data
        fields = ['user', 'City', 'Month','Year','City_Group_BigCities', 'City_Group_Other','Type_DT','Type_FC',
                  'Type_IL','P2', 'P6', 'P28', 'P27', 'P22','P23','prediction']
