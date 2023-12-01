from knox.views import LoginView as KnoxLoginView
from rest_framework import viewsets, mixins
from rest_framework import filters, permissions
from rest_framework import status
from rest_framework.response import Response
from rest_framework_extensions.mixins import NestedViewSetMixin
from .serializers import ApplicationProfileSerializer, UserSerializer
from .models import ApplicationProfile
from django.contrib.auth import get_user_model
from knox.views import LoginView as KnoxLoginView
from rest_framework.authentication import BaseAuthentication

class PasswordAuthentication(BaseAuthentication):
    def __check_password(self, email, password):
        try:
            user = get_user_model().objects.get(email=email)
            if user.check_password(password):
                return user
            else:
                return False
        except get_user_model().DoesNotExist:
            return False
        
    def authenticate(self, request):
        print(dir(request), request.data.get(get_user_model().USERNAME_FIELD), request.data.get('password'))
        user = self.__check_password(request.data.get(get_user_model().USERNAME_FIELD), request.data.get('password'))
        print(user)
        if user:
            return (user, None)
        else:
            return None

class LoginView(KnoxLoginView):
    authentication_classes=[PasswordAuthentication,]
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        if request.user.is_authenticated:
            return super(LoginView, self).post(request, format=None)
        return Response({"message": "Authentication failed"}, status=status.HTTP_403_FORBIDDEN)


class UserViewSet(NestedViewSetMixin, mixins.RetrieveModelMixin, mixins.ListModelMixin, mixins.CreateModelMixin, viewsets.GenericViewSet):
    serializer_class = UserSerializer
    filter_backends = [filters.OrderingFilter]
    permission_classes = []
    ordering_fields = '__all__'

    def get_queryset(self):
        queryset = get_user_model().objects.all()
        return self.filter_queryset_by_parents_lookups(queryset)
    def get_permissions(self):
        return super().get_permissions()

class ApplicationProfileViewSet(NestedViewSetMixin, viewsets.ModelViewSet):
    """
    API endpoint that allows jobs to be viewed or edited.
    """
    queryset = ApplicationProfile.objects.all()
    serializer_class = ApplicationProfileSerializer
    filter_backends = [filters.OrderingFilter]
    permission_classes = [permissions.IsAuthenticated,]
    ordering_fields = '__all__'
    ordering = ['-created_at']

    def get_queryset(self):
        # print('ApplicationProfile', self.kwargs)
        queryset = ApplicationProfile.objects.all()
        return self.filter_queryset_by_parents_lookups(queryset)
    def get_permissions(self):
        return super().get_permissions()