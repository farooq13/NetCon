# Generated by Django 5.0.6 on 2024-08-01 17:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('social', '0005_alter_userprofile_bio_alter_userprofile_location_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='bio',
            field=models.TextField(blank=True, max_length=200, null=True),
        ),
    ]