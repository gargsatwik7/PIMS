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

# Common mixin for auto-filling created_by and updated_by
class AutoUserAdmin(admin.ModelAdmin):
    exclude = ('created_by', 'updated_by')

    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user.username
        obj.updated_by = request.user.username
        obj.save()


@admin.register(Project)
class ProjectAdmin(AutoUserAdmin):
    list_display = ('name', 'type', 'status', 'start_date', 'end_date', 'created_by', 'updated_by', 'updated_at')
    list_filter = ('type', 'status', 'start_date')
    search_fields = ('name', 'client__Client_name')


@admin.register(ProjectCredential)
class ProjectCredentialAdmin(AutoUserAdmin):
    list_display = ('project', 'created_by', 'updated_by', 'updated_at')
    search_fields = ('project__name',)


@admin.register(ProjectActivity)
class ProjectActivityAdmin(AutoUserAdmin):
    list_display = ('project', 'status', 'activity_from', 'activity_to')
    list_filter = ('status', 'activity_from')
    search_fields = ('project__name',)


@admin.register(Team)
class TeamAdmin(AutoUserAdmin):
    list_display = ('team_type', 'created_by', 'updated_by', 'updated_at')
    list_filter = ('team_type',)


@admin.register(Member)
class MemberAdmin(AutoUserAdmin):
    list_display = ('name', 'role', 'created_by', 'updated_by', 'updated_at')
    search_fields = ('name', 'role')
    list_filter = ('role',)


@admin.register(Client)
class ClientAdmin(AutoUserAdmin):
    list_display = ('Client_name','created_by', 'updated_by', 'updated_at')
    search_fields = ('Client_name',)


@admin.register(MemberAssigned)
class MemberAssignedAdmin(AutoUserAdmin):
    list_display = ('member', 'project', 'assigned_from', 'assigned_to', 'is_active')
    list_filter = ('is_active', 'assigned_from')
    search_fields = ('member__name', 'project__name')
