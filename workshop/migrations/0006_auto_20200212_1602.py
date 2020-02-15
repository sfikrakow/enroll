# Generated by Django 3.0.2 on 2020-02-12 16:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workshop', '0005_auto_20200209_1757'),
    ]

    operations = [
        migrations.AlterField(
            model_name='workshopregistration',
            name='accepted',
            field=models.CharField(choices=[('AC', 'Accepted'), ('RE', 'Rejected'), ('WA', 'Waiting')], default='WA', max_length=2),
        ),
    ]