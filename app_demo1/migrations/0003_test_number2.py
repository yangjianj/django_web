# Generated by Django 2.2.2 on 2019-09-18 14:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_demo1', '0002_test_number1'),
    ]

    operations = [
        migrations.AddField(
            model_name='test',
            name='number2',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
