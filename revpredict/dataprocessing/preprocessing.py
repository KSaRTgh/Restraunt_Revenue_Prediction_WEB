from .models import *
import pandas as pd
import numpy as np
from sklearn import preprocessing
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.compose import ColumnTransformer
import sqlite3


def add_RawData(df, **kwargs):
    request = kwargs['request']
    df = df.rename(
        columns={"Id": "original_id", "Open Date": "Open_Date", "City Group": "City_Group"})

    errtext = ''
    rawData_cols = [f.name for f in RawData._meta.get_fields()]
    isError = False
    for col in df.columns:
        if col not in rawData_cols:
            isError = True
            errtext += f'Error, {col} is not in RawData model; \r\n'
    if isError:
        return errtext

    # save to db
    added_data = RawData.objects.bulk_create(
        RawData(**vals, user=request.user) for vals in df.to_dict('records'))

    pks = []
    for obj in added_data:
        pks.append(obj.pk)
    # print('Pks of RawData', pks)

    qs_added_data = RawData.objects.filter(pk__in=pks)

    return qs_added_data


def preprocess(data, **kwargs):
    request = kwargs['request']

    df = pd.DataFrame(list(data.values()))
    print('On create\n', df.head())


    df = df.drop([ 'original_id', 'revenue', 'user_id'], axis=1) #"id",

    df = time_feature_convert(df)

    df = City_label_encode_transform(df)
    print('After label encoding\n', df.head())

    df = onehot_encode_transform(df=df, cols=['City_Group', 'Type'])
    print('After one-hot-encoding\n', df.head())


    features_to_standardize = ["P2", "P6", "P28", "P27", "P22", "P23"]
    features_to_drop = ["P1", "P2", "P3", "P4", "P5", "P6", "P7", "P8", "P9", "P10", "P11", "P12", "P13", "P14", "P15",
                        "P16", "P17", "P18", "P19", "P20",
                        "P21", "P22", "P23", "P24", "P25", "P26", "P27", "P28", "P29", "P30", "P31", "P32", "P33",
                        "P34", "P35", "P36", "P37"]

    scalered_data_df = scaler(df, features_to_standardize)
    df = df.drop(features_to_drop, axis=1)
    df[features_to_standardize] = scalered_data_df[features_to_standardize]

    print('After standartize\n', df.head())


    if 'City_Group_Big Cities' in df:
        df = df.rename(
            columns={"City_Group_Big Cities": "City_Group_BigCities"})

    # error processing
    errtext = ''
    Data_cols = [f.name for f in Data._meta.get_fields()]
    isError = False
    for col in df.columns:
        if col not in Data_cols:
            isError = True
            errtext += f'Error, {col} is not in Data model; \r\n'
    if isError:
        return errtext

    print('After error processing\n', df.head())

    df = df.rename(columns={"id": "raw_id"})
    print('After rename id to raw_id\n', df.head())

    # save to db
    preproccessed_data = Data.objects.bulk_create(
        Data(**vals, user=request.user) for vals in df.to_dict('records'))

    pks = []
    for obj in preproccessed_data:
        pks.append(obj.pk)
    # print('Pks of RawData', pks)

    qs_preproccessed_data = RawData.objects.filter(pk__in=pks)
    # print('norm: ', qs_preproccessed_data)

    # print(df.head)
    return qs_preproccessed_data


def time_feature_convert(dataset):
    dataset['Date'] = pd.to_datetime(dataset['Open_Date'])
    dataset['Month'] = [x.month for x in dataset['Date']]
    dataset['Year'] = [x.year for x in dataset['Date']]
    dataset.drop(['Open_Date', 'Date'], axis=1, inplace=True)
    return dataset


# define the function for label and one-hot encoding
def label_encode_transform_orig(df, cols):
    cols = cols
    le = preprocessing.LabelEncoder()
    df[cols] = df[cols].apply(le.fit_transform)
    return df


def City_label_encode_transform(df):
    cities = {'Adana': 0, 'Afyonkarahisar': 1, 'Aksaray': 2, 'Amasya': 3, 'Ankara': 4, 'Antalya': 5, 'Artvin': 6,
              'Aydın': 7, 'Balıkesir': 8, 'Batman': 9, 'Bilecik': 10, 'Bolu': 11, 'Bursa': 12, 'Denizli': 13,
              'Diyarbakır': 14, 'Düzce': 15, 'Edirne': 16, 'Elazığ': 17, 'Erzincan': 18, 'Erzurum': 19, 'Eskişehir': 20,
              'Gaziantep': 21, 'Giresun': 22, 'Hatay': 23, 'Isparta': 24, 'Kahramanmaraş': 25, 'Karabük': 26,
              'Kars': 27, 'Kastamonu': 28, 'Kayseri': 29, 'Kocaeli': 30, 'Konya': 31, 'Kütahya': 32, 'Kırklareli': 33,
              'Kırıkkale': 34, 'Kırşehir': 35, 'Malatya': 36, 'Manisa': 37, 'Mardin': 38, 'Mersin': 39, 'Muğla': 40,
              'Nevşehir': 41, 'Niğde': 42, 'Ordu': 43, 'Osmaniye': 44, 'Rize': 45, 'Sakarya': 46, 'Samsun': 47,
              'Siirt': 48, 'Sivas': 49, 'Tanımsız': 50, 'Tekirdağ': 51, 'Tokat': 52, 'Trabzon': 53, 'Uşak': 54,
              'Yalova': 55, 'Zonguldak': 56, 'Çanakkale': 57, 'Çankırı': 58, 'Çorum': 59, 'İstanbul': 60, 'İzmir': 61,
              'Şanlıurfa': 62}

    for index, row in df.iterrows():
        if row['City'] in cities.keys():
            df.at[index, 'City'] = cities[row['City']]
            #df.iloc[index] = cities[row['City']]

        else:
            df.at[index, 'City'] = -1

    return df


def onehot_encode_transform(df, cols):
    cols = cols
    df = pd.get_dummies(df, columns=cols)
    return df


def scaler(df, features_to_standardize):
    sc = StandardScaler()
    # sc = MinMaxScaler()
    data = df[features_to_standardize]
    scalered_data = sc.fit_transform(data.T)
    scalered_data_df = pd.DataFrame(scalered_data.T, columns=[features_to_standardize])

    return scalered_data_df
