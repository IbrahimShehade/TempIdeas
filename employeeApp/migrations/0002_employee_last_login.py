# Generated by Django 4.2.3 on 2023-07-12 07:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employeeApp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='employee',
            name='last_login',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
