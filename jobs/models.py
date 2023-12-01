from django.db import models
from django.contrib.postgres.indexes import GinIndex
from django.contrib.postgres.search import SearchVectorField, SearchVector
from ckeditor.fields import RichTextField
from django.conf import settings
import uuid
import nh3
from django.utils import timezone
# Create your models here.
class Employer(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    logo = models.CharField(blank=True)
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    address = models.CharField(max_length=200)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.DO_NOTHING,
        blank=True,
    )

    def __str__(self) -> str:
        return self.name


MODES_OF_WORK = [
    ('IN-OFFICE', 'IN-OFFICE'),
    ('HYBRID', 'HYBRID'),
    ('REMOTE', 'REMOTE'),
]

SALARY_PERIOD_DEFAULT = 'MONTHLY'
SALARY_PERIODS = [
    ('WEEKLY', 'WEEKLY'),
    ('MONTHLY', 'MONTHLY'),
    ('YEARLY', 'YEARLY'),
]

POST_STATUS_DEFAULT = 'DRAFT'
POST_STATUSES = [
    ('DRAFT', 'DRAFT'),
    ('PUBLISHED', 'PUBLISHED'),
    ('UNPUBLISHED', 'UNPUBLISHED'),
]


class Job(models.Model):
    jobs = models.Manager()
    class Meta:
        # The search index pointing to our actual search field.
        indexes = [GinIndex(fields=["search"])]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    employer = models.ForeignKey(
        Employer,
        on_delete=models.DO_NOTHING,
        blank=True,
    )
    title = models.CharField(max_length=200)
    is_application_native = models.BooleanField(default=False)
    is_salary_included = models.BooleanField(default=False)
    salary = models.IntegerField(blank=True)
    salary_period = models.CharField(choices=SALARY_PERIODS, default=SALARY_PERIOD_DEFAULT)
    salary_currency = models.CharField(max_length=3, blank=True)
    description = RichTextField()
    mode_of_work = models.CharField(choices=MODES_OF_WORK)
    work_location = models.CharField(max_length=200)
    minimum_experience = models.DecimalField(max_digits=4, decimal_places=1, blank=False)
    application_url = models.URLField(blank=True)
    application_email = models.EmailField(blank=True)
    post_status = models.CharField(choices=POST_STATUSES, default=POST_STATUS_DEFAULT)
    online_until = models.DateTimeField(null=True, blank=True)
    search = SearchVectorField(null=True, blank=True)

    def save(self, *args, **kwargs):
        self.description = nh3.clean(self.description)
        super().save(*args, **kwargs)
        Job.jobs.filter(pk=self.id).update(search=(
            SearchVector('title', weight='A') 
            + SearchVector('description', weight='B')
        ))

    def publish_job(self):
        if self.post_status != 'PUBLISHED':
            self.post_status = 'PUBLISHED'
            self.online_until = timezone.now() + timezone.timedelta(days=32)
            return self.save()
        else:
            return None

    def unpublish_job(self):
        if self.post_status == 'PUBLISHED':
            self.post_status = 'UNPUBLISHED'
            self.online_until = None
            return self.save()
        else:
            return None


    def __str__(self) -> str:
        return self.title

EDUCATION_LEVELS = [
    ('PRIMARY', 'PRIMARY'),
    ('SECONDARY', 'SECONDARY'),
    ('TERTIARY', 'TERTIARY'),
    ('GRADUATE', 'GRADUATE'),
    ('POST-GRADUATE', 'POST-GRADUATE')
    ]

APPLICATION_STATUSES = [
    ('APPLIED', 'APPLIED'),
    ('IN-REVIEW', 'IN-REVIEW'),
    ('REJECTED', 'REJECTED'),
    ('OFFERED', 'OFFERED'),
    ]
class Application(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    job = models.ForeignKey(Job, on_delete=models.DO_NOTHING)
    applicant = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.DO_NOTHING,
    )
    resume_link = models.URLField(blank=True)
    details = models.TextField(blank=True)
    employer_message = models.TextField(blank=True)
    status = models.CharField(choices=APPLICATION_STATUSES)
    education_level = models.CharField(choices=EDUCATION_LEVELS, blank=False)
    years_of_experience = models.DecimalField(max_digits=4, decimal_places=1, blank=False)
