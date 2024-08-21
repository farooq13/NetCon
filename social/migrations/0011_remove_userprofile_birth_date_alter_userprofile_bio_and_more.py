# Generated by Django 5.0.6 on 2024-08-20 16:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('social', '0010_alter_userprofile_bio'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='birth_date',
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='bio',
            field=models.TextField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='location',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='picture',
            field=models.ImageField(default='uploads/profile_pictures/avatar.svg', upload_to='uploads/profile_pictures'),
        ),
    ]
