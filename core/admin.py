from django.contrib import admin
from .models import (
    Project,
    Team,
    Member,
    Client,
    MemberAssigned,
    ProjectActivity,
    ProjectCredential,
)


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'status', 'start_date', 'end_date', 'created_by', 'updated_by', 'updated_at')
    list_filter = ('type', 'status', 'start_date')
    search_fields = ('name', 'client__Client_name')


@admin.register(ProjectCredential)
class ProjectCredentialAdmin(admin.ModelAdmin):
    list_display = ('project', 'key', 'created_by', 'updated_by', 'updated_at')
    search_fields = ('project__name', 'key')


@admin.register(ProjectActivity)
class ProjectActivityAdmin(admin.ModelAdmin):
    list_display = ('project', 'status', 'activity_from', 'activity_to')
    list_filter = ('status', 'activity_from')
    search_fields = ('project__name',)


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ('team_name', 'team_type', 'created_by', 'updated_by', 'updated_at')
    search_fields = ('team_name',)
    list_filter = ('team_type',)


@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = ('name', 'role', 'created_by', 'updated_by', 'updated_at')
    search_fields = ('name', 'role')
    list_filter = ('role',)


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('Client_name', 'company_name', 'created_by', 'updated_by', 'updated_at')
    search_fields = ('Client_name', 'company_name')


@admin.register(MemberAssigned)
class MemberAssignedAdmin(admin.ModelAdmin):
    list_display = ('member', 'project', 'assigned_from', 'assigned_to', 'is_active')
    list_filter = ('is_active', 'assigned_from')
    search_fields = ('member__name', 'project__name')
