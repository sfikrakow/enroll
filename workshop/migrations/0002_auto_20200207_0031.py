# Generated by Django 3.0.2 on 2020-02-07 00:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('workshop', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='workshopregistration',
            old_name='participant_id',
            new_name='participant',
        ),
        migrations.RenameField(
            model_name='workshopregistration',
            old_name='workshops_id',
            new_name='workshop',
        ),
    ]