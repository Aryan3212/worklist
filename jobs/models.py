from django.db import models
from django.core.validators import RegexValidator
from django.contrib.postgres.indexes import GinIndex
from django.contrib.postgres.search import SearchVectorField, SearchVector
from ckeditor.fields import RichTextField
import nh3
# Create your models here.

alphanumeric_punctuation_regex = '^[a-zA-Z0-9 _.,\-+=`~\|><@#$%^&*()!"\'/$]*$'
class Job(models.Model):
    jobs = models.Manager()
    class Meta:
        # The search index pointing to our actual search field.
        indexes = [GinIndex(fields=["search"])]
    
    title = models.CharField(max_length=200,  validators=[
        RegexValidator(
            regex=alphanumeric_punctuation_regex,
            message='Only alphanumeric characters are allowed.',
            code='invalid_characters'
        )
    ])
    description = RichTextField()
    location = models.CharField(max_length=200,  validators=[
        RegexValidator(
            regex=alphanumeric_punctuation_regex,
            message='Only alphanumeric characters are allowed.',
            code='invalid_characters'
        )
    ])
    company_name = models.CharField(max_length=200,  validators=[
        RegexValidator(
            regex=alphanumeric_punctuation_regex,
            message='Only alphanumeric characters are allowed.',
            code='invalid_characters'
        )
    ])
    minimum_experience = models.IntegerField(default=0)
    application_url = models.URLField(blank=True)
    application_email = models.EmailField(blank=True)
    date_added = models.DateTimeField("Date Published", auto_now_add=True, blank=True)
    search = SearchVectorField(null=True)

    def save(self, *args, **kwargs):
        self.description = nh3.clean(self.description)
        super().save(*args, **kwargs)
        Job.jobs.filter(pk=self.id).update(search=(
            SearchVector('title', weight='A') 
            + SearchVector('description', weight='B')
            + SearchVector('location', weight='C')
            + SearchVector('company_name', weight='D')
        ))

    def __str__(self) -> str:
        return self.title + " " + self.company_name


