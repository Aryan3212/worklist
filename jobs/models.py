from django.db import models
from django.core.validators import RegexValidator
from ckeditor.fields import RichTextField
import nh3
# Create your models here.


alphanumericpunctuation_regex = '^[a-zA-Z0-9 _.,\-+=`~\|><@#$%^&*()!"\'/$]*$'
class Job(models.Model):
    title = models.CharField(max_length=200,  validators=[
        RegexValidator(
            regex=alphanumericpunctuation_regex,
            message='Only alphanumeric characters are allowed.',
            code='invalid_characters'
        )
    ])
    description = RichTextField()
    location = models.CharField(max_length=200,  validators=[
        RegexValidator(
            regex=alphanumericpunctuation_regex,
            message='Only alphanumeric characters are allowed.',
            code='invalid_characters'
        )
    ])
    company_name = models.CharField(max_length=200,  validators=[
        RegexValidator(
            regex=alphanumericpunctuation_regex,
            message='Only alphanumeric characters are allowed.',
            code='invalid_characters'
        )
    ])
    minimum_experience = models.IntegerField(default=0)
    application_url = models.URLField(blank=True)
    application_email = models.EmailField(blank=True)
    date_added = models.DateTimeField("Date Published", auto_now_add=True, blank=True)

    def save(self, *args, **kwargs):
        self.description = nh3.clean(self.description)
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.title + " " + self.company_name


