# Generated by Django 3.0.5 on 2020-07-15 10:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0011_dataset_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='dataset',
            name='dataslug',
            field=models.TextField(null=True),
        ),
    ]
