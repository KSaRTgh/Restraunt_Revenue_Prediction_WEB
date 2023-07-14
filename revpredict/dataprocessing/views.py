import pandas as pd
from django.contrib import messages
from django.shortcuts import render, redirect
from django_tables2 import RequestConfig
from django.contrib.auth.decorators import login_required
import sklearn
from joblib import dump, load
from dataprocessing.forms import *

@login_required
def dataprocessing(request):

    db_view_table = db_viewTable(Data.objects.filter(user__id=request.user.id))
    method_post = False
    if request.method == 'POST':
        method_post= True

        pks = request.POST.getlist("selection")
        selected_objects = Data.objects.filter(pk__in=pks)
        #selected_objects.update()

        #work with model
        predict(selected_objects)


        predictions_table = predictionsTable(selected_objects)
        return render(request, 'dataprocessing/dataprocessing.html',
                      {'table': db_view_table, 'predictions_table': predictions_table, 'method_post': method_post})

    else:
        RequestConfig(request).configure(db_view_table)
    return render(request, 'dataprocessing/dataprocessing.html', {'table': db_view_table, 'method_post': method_post})


@login_required
def add_to_db(request):

    if request.method == 'POST':
        data_form = AddToDbForm(request.POST, initial={'user': request.user})
        data_form.fields['user'].disabled = True

        print(request.user.id)
        if data_form.is_valid():
            data_form.save()
            messages.success(request, 'successfully added')
            return redirect('add-to-db')
    else:
        data_form = AddToDbForm(initial={'user': request.user})
        data_form.fields['user'].disabled = True

    return render(request, 'dataprocessing/add-to-db.html', {'form': data_form})


def predict(selected_objects):
    df = pd.DataFrame(list(selected_objects.values('City', 'Month', 'Year', 'City_Group_BigCities',
                                                   'City_Group_Other', 'Type_DT', 'Type_FC', 'Type_IL',
                                                   'P2', 'P6', 'P28', 'P27', 'P22', 'P23')))

    df = df.rename(columns={"City_Group_BigCities": "City Group_Big Cities", "City_Group_Other": "City Group_Other"})

    ML_model = load('ML_model.joblib')
    predicts = ML_model.predict(df)

    for i in range(len(selected_objects)):
        selected_objects[i].prediction = predicts[i]
        selected_objects[i].save()

