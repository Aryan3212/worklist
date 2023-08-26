from django.db import models

# Create your models here.

class Job(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    location = models.CharField(max_length=200)
    company_name = models.CharField(max_length=200)
    minimum_experience = models.IntegerField(default=0)
    application_url = models.URLField()
    date_added = models.DateTimeField("Date Published")

    def __str__(self) -> str:
        return self.title + " " + self.company_name


