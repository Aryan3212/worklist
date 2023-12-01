from .models import Job, Application, Employer
from rest_framework import serializers
from users.serializers import UserSerializer

class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = '__all__'

class ApplicationSerializer(serializers.ModelSerializer):
    applicant = UserSerializer(read_only=True, many=False)
    class Meta:
        model = Application
        fields = ['id', 'created_at', 'updated_at', 'applicant', 'resume_link',]

class JobApplicationSerializer(serializers.ModelSerializer):
    owner = UserSerializer(source="job.employer.owner", read_only=True, many=False)
    class Meta:
        model = Application
        fields = ['id', 'created_at', 'updated_at', 'applicant', 'resume_link', 'applicant', 'owner']

class EmployerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employer
        fields = '__all__'