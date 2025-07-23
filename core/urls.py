from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views_auth import CustomAuthToken
from .views import (
    ClientViewSet, ProjectViewSet, ProjectCredentialViewSet, TeamViewSet,
    MemberViewSet, MemberAssignedViewSet, ProjectActivityViewSet
)

router = DefaultRouter()
router.register(r'clients', ClientViewSet)
router.register(r'projects', ProjectViewSet)
router.register(r'credentials', ProjectCredentialViewSet)
router.register(r'teams', TeamViewSet)
router.register(r'members', MemberViewSet)
router.register(r'assignments', MemberAssignedViewSet)
router.register(r'project-activities', ProjectActivityViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('api-token-auth/', CustomAuthToken.as_view(), name='custom_token_auth'),
]
