# Generated by Django 3.2.8 on 2021-12-06 19:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hw_session', '0021_alter_session_data_break_interval'),
    ]

    operations = [
        migrations.AlterField(
            model_name='session_data',
            name='break_interval',
            field=models.FloatField(choices=[(0.016, '1min'), (0.25, '15mins'), (0.5, '30mins'), (0.75, '45mins'), (1, '1hr'), (1.25, '1hr 15mins'), (1.5, '1hr 30mins')], default=0.016, max_length=30, null=True),
        ),
    ]
