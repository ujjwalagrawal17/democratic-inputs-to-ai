# Generated by Django 3.2.19 on 2023-06-15 09:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='wrong_mpin_tries_count',
        ),
        migrations.AddField(
            model_name='userprofile',
            name='flag_aadhar_card_verified',
            field=models.BooleanField(default=False),
        ),
    ]
