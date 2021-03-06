# Generated by Django 3.0.2 on 2020-02-09 14:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('workshop', '0002_auto_20200207_0031'),
    ]

    operations = [
        migrations.CreateModel(
            name='RegistrationAnswer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=300)),
                ('workshop_registration', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='workshop.WorkshopRegistration')),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=200)),
                ('workshop', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='workshop.Workshop')),
            ],
        ),
        migrations.CreateModel(
            name='DefaultAnswer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=300)),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='workshop.Question')),
            ],
        ),
    ]
