from django.db.models import Q
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank, TrigramSimilarity
from .models import Job, Application, Employer
from rest_framework import mixins, viewsets
from rest_framework import filters, permissions
from .serializers import JobSerializer, EmployerSerializer, ApplicationSerializer, JobApplicationSerializer
from rest_framework_extensions.mixins import NestedViewSetMixin
from .permissions import IsApplicationOwner, IsJobApplicationOwner, IsJobOwner
class ListJobs(NestedViewSetMixin, mixins.ListModelMixin, mixins.RetrieveModelMixin,mixins.CreateModelMixin, viewsets.GenericViewSet):
    """
    API endpoint that allows jobs to be viewed or edited.
    """
    serializer_class = JobSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = '__all__'
    ordering = ['-created_at']
    def get_queryset(self):
        queryset = Job.jobs.all()
        if self.request.query_params.get('search'):
            search = self.request.query_params.get('search')
            vector = SearchVector('search')
            query = SearchQuery(search)
            similarity = TrigramSimilarity('search', search)
            queryset = queryset.annotate(
                rank=SearchRank(vector, query),
                similarity=similarity
            ).filter(Q(search=query) | Q(similarity_gt=0.3)).order_by("-rank", "-similarity")
        return self.filter_queryset_by_parents_lookups(queryset)
    
    def get_serializer(self, *args, **kwargs):
        return super().get_serializer(*args, **kwargs)
    
    def get_permissions(self):
        if self.basename == 'users-employers-jobs':
            return [permissions.IsAuthenticated(), IsJobOwner()]
        elif self.basename == 'jobs':
            return []
        
class ListRetrieveEmployers(NestedViewSetMixin, mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """
    API endpoint that allows jobs to be viewed or edited.
    """
    queryset = Employer.objects.all()
    serializer_class = EmployerSerializer
    filter_backends = [filters.OrderingFilter]
    permission_classes = [permissions.IsAuthenticated,]
    ordering_fields = '__all__'
    ordering = ['-created_at']

    def get_permissions(self):
        return super().get_permissions()


class ApplicationsViewSet(NestedViewSetMixin, viewsets.ModelViewSet):
    """
    API endpoint that allows jobs to be viewed or edited.
    """
    queryset = Application.objects.all()
    filter_backends = [filters.OrderingFilter]
    ordering_fields = '__all__'
    ordering = ['-created_at']

    def get_serializer_class(self):
        if self.basename == 'users-employers-jobs-applications':
            return JobApplicationSerializer
        elif self.basename == 'users-applications':
            return ApplicationSerializer

    def get_permissions(self):
        if self.basename == 'users-employers-jobs-applications':
            return [permissions.IsAuthenticated(),IsJobApplicationOwner()]
        elif self.basename == 'users-applications':
            return [permissions.IsAuthenticated(),IsApplicationOwner()]
