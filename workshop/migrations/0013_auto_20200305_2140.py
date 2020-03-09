# Generated by Django 3.0.3 on 2020-03-05 21:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workshop', '0012_auto_20200218_1909'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='answeroption',
            options={'ordering': ['id']},
        ),
        migrations.AlterModelOptions(
            name='question',
            options={'ordering': ['id']},
        ),
        migrations.AlterModelOptions(
            name='registrationanswer',
            options={'ordering': ['id']},
        ),
        migrations.AlterModelOptions(
            name='workshop',
            options={'ordering': ['id']},
        ),
        migrations.AlterField(
            model_name='workshopregistration',
            name='accepted',
            field=models.CharField(choices=[('AC', 'Accepted'), ('RE', 'Rejected'), ('WA', 'Waiting'), ('WL', 'Waiting List')], default='WA', max_length=2),
        ),
        migrations.AlterUniqueTogether(
            name='registrationanswer',
            unique_together={('workshop_registration', 'question')},
        ),
    ]