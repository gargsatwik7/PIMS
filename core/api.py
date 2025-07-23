from rest_framework import viewsets
from rest_framework.routers import DefaultRouter
from .models import Client, Project, ProjectCredential, Team, Member, MemberAssigned, ProjectActivity
from .serializers import (
    ClientSerializer, ProjectSerializer, ProjectCredentialSerializer,
    TeamSerializer, MemberSerializer, MemberAssignedSerializer,
    ProjectActivitySerializer
)

class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated
from .permissions import IsManagerOrReadOnly
from .filters import ProjectFilter

class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated, IsManagerOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_class = ProjectFilter

class ProjectCredentialViewSet(viewsets.ModelViewSet):
    queryset = ProjectCredential.objects.all()
    serializer_class = ProjectCredentialSerializer

class TeamViewSet(viewsets.ModelViewSet):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer

class MemberViewSet(viewsets.ModelViewSet):
    queryset = Member.objects.all()
    serializer_class = MemberSerializer

class MemberAssignedViewSet(viewsets.ModelViewSet):
    queryset = MemberAssigned.objects.all()
    serializer_class = MemberAssignedSerializer

class ProjectActivityViewSet(viewsets.ModelViewSet):
    queryset = ProjectActivity.objects.all()
    serializer_class = ProjectActivitySerializer

router = DefaultRouter()
router.register(r'clients', ClientViewSet)
router.register(r'projects', ProjectViewSet)
router.register(r'credentials', ProjectCredentialViewSet)
router.register(r'teams', TeamViewSet)
router.register(r'members', MemberViewSet)
router.register(r'assignments', MemberAssignedViewSet)
router.register(r'activities', ProjectActivityViewSet)
