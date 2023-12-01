from django.urls import include, path
from django.contrib import admin
from knox import views as knox_views
from users.views import LoginView
import jobs.views as jobs_views
import users.views as users_views
import payments.views as payments_views
from rest_framework_extensions.routers import ExtendedDefaultRouter as DefaultRouter

router = DefaultRouter()
user_router = router.register(r'users', users_views.UserViewSet, basename='users')
user_router.register(r'applications',
        jobs_views.ApplicationsViewSet,
        basename='users-applications',
        parents_query_lookups=['applicant'])

user_router.register(
    r'employers',
    jobs_views.ListRetrieveEmployers,
    basename='user-employers',
    parents_query_lookups=['owner']
    ).register(
        r'jobs',
        jobs_views.ListJobs,
        basename='users-employers-jobs',
        parents_query_lookups=['employer__owner', 'employer']
    ).register(
        r'applications',
        jobs_views.ApplicationsViewSet,
        basename='users-employers-jobs-applications',
        parents_query_lookups=['job__employer__owner', 'job__employer', 'job']
    )

router.register(r'jobs', jobs_views.ListJobs, basename='jobs')
router.register(r'employers', jobs_views.ListRetrieveEmployers, basename='employers')
router.register(r'applications', jobs_views.ApplicationsViewSet, basename='applications')
router.register(r'payments', payments_views.PaymentsViewSet, basename='payments')
# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
    path('admin/', admin.site.urls),
    path('login/', LoginView.as_view()),
    path('logout/', knox_views.LogoutView.as_view()),
    path('logoutall/', knox_views.LogoutAllView.as_view()),
    path('api/', include('rest_framework.urls', namespace='rest_framework'))
]
