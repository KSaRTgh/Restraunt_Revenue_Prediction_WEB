import types
import logging
import pandas as pd
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, reverse
from django_tables2 import RequestConfig
from django.contrib.auth.decorators import login_required
import sklearn
from joblib import dump, load
from .forms import *
from .preprocessing import *

#logger = logging.getLogger('main')
loggerdj = logging.getLogger('django')

@login_required
def add_raw_to_db(request):
    try:
        loggerdj.info("add_raw_to_db view call")
        if request.method == 'POST':
            data_form = AddRawToDbForm(request.POST, initial={'user': request.user})
            data_form.fields['user'].disabled = True

            if data_form.is_valid():
                inst = data_form.save()
                qs = RawData.objects.filter(pk=inst.pk)
                preprocessed_data = preprocess(data=qs, request=request)
                messages.success(request, 'Successfully added to RawData')
                return redirect('add-raw-to-db')
            logger.warning("Invalid data form")
        else:
            data_form = AddRawToDbForm(initial={'user': request.user})
            data_form.fields['user'].disabled = True

        return render(request, 'dataprocessing/add-to-db.html', {'form': data_form})
    except Exception as e:
        logger.exception("Exception occuried in add_raw_to_db view")


@login_required
def add_to_db(request):
    try:
        logger.info("add_to_db function call")
        if request.method == 'POST':
            data_form = AddToDbForm(request.POST, initial={'user': request.user})
            data_form.fields['user'].disabled = True

            if data_form.is_valid():
                inst = data_form.save()
                print(inst.pk)
                messages.success(request, 'successfully added')
                logger.info("Successfully added to Data table")
                return redirect('add-to-db')
            #TODO: error message
        else:
            data_form = AddToDbForm(initial={'user': request.user})
            data_form.fields['user'].disabled = True

        return render(request, 'dataprocessing/add-to-db.html', {'form': data_form})
    except Exception as e:
        logger.exception("Exception occured in add_raw_to_db view")
#loads data from csv and saves into RawData
@login_required
def read_from_csv(request):
    try:
        logger.info("read_from_csv function call")
        if request.method == 'POST':
            load_form = load_csvForm(request.POST, request.FILES)

            if load_form.is_valid():
                file = request.FILES['file']
                df = pd.read_csv(file)

                added_data = add_RawData(df=df, request=request)
                if type(added_data) == str:
                    messages.warning(request, added_data)
                    return redirect('read-from-csv')

                preprocessed_data = preprocess(data=added_data, request=request)
                if type(preprocessed_data) == str:
                    messages.warning(request, preprocessed_data)
                    return redirect('read-from-csv')

                data_table = RawDataTable(added_data)
                context ={
                    'form': load_form,
                    'file': file,
                    'method_post': True,
                    'table': data_table
                }

                messages.success(request, f'Successfully loaded from {file.name}')
                logger.info(f'Successfully loaded from {file.name}')
                #return render(request,'dataprocessing/read-from-csv.html',context )
                return redirect('make-predictions')
        else:
            load_form = load_csvForm()
        return render(request,'dataprocessing/read-from-csv.html',{'form':load_form})
    except Exception as e:
        logger.exception("Exception occuried in read_from_csv")

@login_required
def make_prediction(request):
    try:
        db_view_table = db_view_rawTable(RawData.objects.filter(user__id=request.user.id))
        RequestConfig(request).configure(db_view_table)
        method_post = False
        if request.method == 'POST':
            method_post= True
            RequestConfig(request).configure(db_view_table)

            pks = request.POST.getlist("selection")
            selected_objects = Data.objects.filter(raw_id__in=pks)

            #work with model
            make_prediction_func(selected_objects)

            predictions_table = predictions_Table(selected_objects)
            return render(request, 'dataprocessing/make_predictions.html',
                          {'table': db_view_table, 'predictions_table': predictions_table, 'method_post': method_post})

        return render(request, 'dataprocessing/make_predictions.html', {'table': db_view_table, 'method_post': method_post})
    except Exception as e:
        logger.exception("Exception occured in make_prediction view")
#TODO: relocate to preprocessing.py
def make_prediction_func(selected_objects):

    df = pd.DataFrame(list(selected_objects.values('City', 'Month', 'Year', 'City_Group_BigCities',
                                                   'City_Group_Other', 'Type_DT', 'Type_FC', 'Type_IL',
                                                   'P2', 'P6', 'P28', 'P27', 'P22', 'P23')))

    df = df.rename(columns={"City_Group_BigCities": "City Group_Big Cities", "City_Group_Other": "City Group_Other"})

    ML_model = load('ML_model.joblib')
    predicts = ML_model.predict(df)

    for i in range(len(selected_objects)):
        selected_objects[i].prediction = predicts[i]
        selected_objects[i].save()
