# Generated by Django 3.0.2 on 2020-02-01 23:49

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Workshop',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('date', models.DateField()),
                ('open', models.BooleanField(default=True)),
                ('auto_response', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='WorkshopRegistration',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(default=django.utils.timezone.now)),
                ('active', models.BooleanField()),
                ('accepted', models.BooleanField()),
                ('participant_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('workshops_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='workshop.Workshop')),
            ],
        ),
    ]