from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenRefreshView,
    TokenVerifyView,
)

from .views import (
    ClientViewSet, ProjectViewSet, ProjectCredentialViewSet, TeamViewSet,
    MemberViewSet, MemberAssignedViewSet, ProjectActivityViewSet,
    CustomTokenObtainPairView,  # ✅ Add this
)

router = DefaultRouter()
router.register(r'clients', ClientViewSet)
router.register(r'projects', ProjectViewSet)
router.register(r'credentials', ProjectCredentialViewSet)
router.register(r'teams', TeamViewSet)
router.register(r'members', MemberViewSet)
router.register(r'assigned-members', MemberAssignedViewSet)
router.register(r'activities', ProjectActivityViewSet)

urlpatterns = router.urls + [
    path('login/', CustomTokenObtainPairView.as_view(), name='custom_token_obtain'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'), 
    # path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),            # optional
]
