# Generated by Django 4.2.4 on 2023-09-01 13:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0005_alter_job_company_name_alter_job_description_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='job',
            name='date_added',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Date Published'),
        ),
    ]
