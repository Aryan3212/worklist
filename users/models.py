from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings
import uuid

class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'password']
    def __str__(self):
        return self.username
    

EDUCATION_LEVELS = [
    ('PRIMARY', 'PRIMARY'),
    ('SECONDARY', 'SECONDARY'),
    ('TERTIARY', 'TERTIARY'),
    ('GRADUATE', 'GRADUATE'),
    ('POST-GRADUATE', 'POST-GRADUATE')
    ]

class ApplicationProfile(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    applicant = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.DO_NOTHING,
        unique=True # May change in the future
    )
    resume_link = models.URLField(blank=True)
    details = models.TextField(blank=True)
    education_level = models.CharField(choices=EDUCATION_LEVELS, blank=False)
    years_of_experience = models.DecimalField(max_digits=4, decimal_places=1, blank=False)