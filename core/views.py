from rest_framework import viewsets
from .models import (
    Client, Project, ProjectCredential, Team,
    Member, MemberAssigned, ProjectActivity
)
from .serializers import (
    ClientSerializer, ProjectSerializer, ProjectCredentialSerializer, TeamSerializer,
    MemberSerializer, MemberAssignedSerializer, ProjectActivitySerializer
)

class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer

class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

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