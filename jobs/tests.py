from django.test import TestCase
from jobs.models import Job, Employer
from users.models import User
# Create your tests here.
class YourTestClass(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass

    def setUp(self):
        user = User.objects.create(**{
        "email": "a@a.com",
        "password": "123",
        })
        employer = Employer.objects.create(
            **{
            "logo": "Rifah",
            "name": "Riwah",
            "description": "Riwfah",
            "address": "a",
            "owner": user
            }
            )
        Job.jobs.create(**{
            "title": "Hello 123",
            "is_application_native": True,
            "is_salary_included": True,
            "salary": 100,
            "salary_period": "WEEKLY",
            "salary_currency": "BDT",
            "description": "<p>Data that is not corrupted!</p>",
            "mode_of_work": "IN-OFFICE",
            "work_location": "Remote",
            "minimum_experience": "1.0",
            "application_url": "https://www.tra.com",
            "application_email": "rifah@rifah.com",
            "employer": employer
            })

    def test_job_publishing(self):
        user = User.objects.get(email="a@a.com")
        self.assertIsNotNone(user)
        employers = Employer.objects.get(owner=user.id)
        print(employers)
        self.assertIsNotNone(employers)
        job = Job.jobs.get(title="Hello 123")
        self.assertEquals(job.post_status, 'DRAFT')
        print(job)
        job.publish_job()
        self.assertEquals(job.post_status, 'PUBLISHED')
        print(job.post_status, job.online_until)
