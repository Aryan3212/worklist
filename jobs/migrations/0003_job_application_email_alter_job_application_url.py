# Generated by Django 4.2.4 on 2023-08-30 16:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0002_job_company_name_job_location_job_minimum_experience_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='job',
            name='application_email',
            field=models.EmailField(blank=True, max_length=254),
        ),
        migrations.AlterField(
            model_name='job',
            name='application_url',
            field=models.URLField(blank=True),
        ),
    ]
