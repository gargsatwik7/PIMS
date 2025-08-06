from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from django.shortcuts import render

def home(request):
    return render(request, 'index.html')

from .models import (
    Client, Project, ProjectCredential, Team,
    Member, MemberAssigned, ProjectActivity
)
from .serializers import (
    ClientSerializer, ProjectSerializer, ProjectCredentialSerializer, TeamSerializer,
    MemberSerializer, MemberAssignedSerializer, ProjectActivitySerializer
)

from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import CustomTokenSerializer

# ✅ Custom permission
from .permissions import ReadOnlyOrAuthenticated


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenSerializer


# ✅ Base class to handle created_by / updated_by
class BaseAutoUserViewSet(viewsets.ModelViewSet):
    permission_classes = [ReadOnlyOrAuthenticated]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user.username)

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user.username)


# ✅ All viewsets inherit from BaseAutoUserViewSet

class ClientViewSet(BaseAutoUserViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer

class ProjectViewSet(BaseAutoUserViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

class ProjectCredentialViewSet(BaseAutoUserViewSet):
    queryset = ProjectCredential.objects.all()
    serializer_class = ProjectCredentialSerializer

class TeamViewSet(BaseAutoUserViewSet):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer

class MemberViewSet(BaseAutoUserViewSet):
    queryset = Member.objects.all()
    serializer_class = MemberSerializer

class MemberAssignedViewSet(BaseAutoUserViewSet):
    queryset = MemberAssigned.objects.all()
    serializer_class = MemberAssignedSerializer

class ProjectActivityViewSet(BaseAutoUserViewSet):
    queryset = ProjectActivity.objects.all()
    serializer_class = ProjectActivitySerializer
