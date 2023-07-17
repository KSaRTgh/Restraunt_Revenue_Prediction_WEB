from django import forms
from django.contrib.auth.models import User
from django.http import request
from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import *
import django_tables2 as tables


class AddToDbForm(forms.ModelForm):
    Month = forms.IntegerField(min_value=1, max_value=12)
    Year = forms.IntegerField(min_value=1000, max_value=2400)
    class Meta:
        model = Data
        fields = ['user', 'City', 'Month','Year','City_Group_BigCities', 'City_Group_Other','Type_DT','Type_FC',
                  'Type_IL','P2', 'P6', 'P28', 'P27', 'P22','P23']


class AddRawToDbForm(forms.ModelForm):
    class Meta:
        model = RawData
        fields = ['user', 'Open_Date', 'City','City_Group','Type','P2', 'P6', 'P28', 'P27', 'P22','P23']


class db_view_rawTable(tables.Table):
    user = tables.Column(visible=False)
    selection = tables.CheckBoxColumn(accessor="pk", attrs={"th__input": {"onclick": "toggle(this)"}},
                                      orderable=False)
    class Meta:
        model = RawData
        fields = ['id', 'City', 'Open_Date','City_Group', 'Type','P2', 'P6', 'P28', 'P27', 'P22','P23']


class predictions_Table(tables.Table):
    user = tables.Column(visible=False)
    selection2 = tables.CheckBoxColumn(accessor="pk", attrs={"th__input": {"onclick": "toggle2(this)"}},
                                      orderable=False)
    Open_Date = tables.Column(accessor='raw.Open_Date')
    City_Group = tables.Column(accessor='raw.City_Group')
    Type = tables.Column(accessor='raw.Type')
    City = tables.Column(accessor='raw.City')

    class Meta:
        model = Data
        fields = [ 'raw_id', 'P2', 'P6', 'P28', 'P27', 'P22',
                  'P23','prediction']
        sequence = ( 'raw_id','Open_Date','City_Group','Type','City')#'id','id',

        verbose_names ={'raw_id':'ID'}

class load_csvForm(forms.Form):
    file = forms.FileField()


class RawDataTable(tables.Table):
    class Meta:
        model = RawData
        #fields = ['user', 'City', 'P2', 'revenue']
        fields = ['original_id','Open_Date','City','City_Group','Type','P2', 'P6', 'P28', 'P27', 'P22','P23','revenue']
