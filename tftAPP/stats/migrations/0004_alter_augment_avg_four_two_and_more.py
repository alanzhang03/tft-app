# Generated by Django 4.1 on 2024-01-28 21:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stats', '0003_data'),
    ]

    operations = [
        migrations.AlterField(
            model_name='augment',
            name='avg_four_two',
            field=models.FloatField(default=0.0),
        ),
        migrations.AlterField(
            model_name='augment',
            name='avg_three_two',
            field=models.FloatField(default=0.0),
        ),
        migrations.AlterField(
            model_name='augment',
            name='avg_total',
            field=models.FloatField(default=0.0),
        ),
        migrations.AlterField(
            model_name='augment',
            name='avg_two_one',
            field=models.FloatField(default=0.0),
        ),
    ]
