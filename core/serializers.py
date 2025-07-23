from rest_framework import serializers
from .models import Client, Project, ProjectCredential, Team, Member, MemberAssigned, ProjectActivity

class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = '__all__'

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__'

class ProjectCredentialSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectCredential
        fields = '__all__'

class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = '__all__'

class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = '__all__'

class MemberAssignedSerializer(serializers.ModelSerializer):
    class Meta:
        model = MemberAssigned
        fields = '__all__'

class ProjectActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectActivity
        fields = '__all__'
