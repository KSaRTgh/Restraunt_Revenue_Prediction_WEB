# Generated by Django 4.2.3 on 2023-07-16 14:47

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dataprocessing', '0002_rawdata'),
    ]

    operations = [
        migrations.AddField(
            model_name='data',
            name='raw',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='dataprocessing.rawdata'),
        ),
        migrations.AlterField(
            model_name='rawdata',
            name='City_Group',
            field=models.CharField(choices=[('Big Cities', 'Big Cities'), ('Other', 'Other')], default='Big Cities', max_length=40),
        ),
        migrations.AlterField(
            model_name='rawdata',
            name='Open_Date',
            field=models.CharField(max_length=20, validators=[django.core.validators.RegexValidator(message='Date should be in format mm/dd/YYYY', regex='^(0[1-9]|1[012])[/](0[1-9]|[12][0-9]|3[01])[/](19|20)\\d\\d$')]),
        ),
        migrations.AlterField(
            model_name='rawdata',
            name='Type',
            field=models.CharField(choices=[('DT', 'DT'), ('FC', 'FC'), ('IL', 'IL')], default='FC', max_length=40),
        ),
        migrations.AlterField(
            model_name='rawdata',
            name='original_id',
            field=models.IntegerField(default=-1),
        ),
    ]
