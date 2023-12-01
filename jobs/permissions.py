from rest_framework import permissions
from .serializers import JobApplicationSerializer

class IsApplicationOwner(permissions.BasePermission):
    def has_permission(self, request, view):
        return super().has_permission(request, view)
    
    def has_object_permission(self, request, view, obj):
        return obj.applicant.id == request.user.id
    
class IsJobApplicationOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.job.employer.owner.id == request.user.id
    
class IsJobOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.employer.owner.id == request.user.id