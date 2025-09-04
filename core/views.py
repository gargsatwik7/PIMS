from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import user_passes_test
from rest_framework import viewsets
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import CustomTokenSerializer
from .models import (
    Client, Project, ProjectCredential, Team,
    Member, MemberAssigned, ProjectActivity
)
from .serializers import (
    ClientSerializer, ProjectSerializer, ProjectCredentialSerializer, TeamSerializer,
    MemberSerializer, MemberAssignedSerializer, ProjectActivitySerializer
)
from .permissions import ReadOnlyOrAuthenticated


# ======================================================
# 🔐 Helper for admin-only pages
# ======================================================
def admin_required(view_func):
    return user_passes_test(lambda u: u.is_authenticated and u.is_staff)(view_func)


# ======================================================
# 🚀 API ViewSets
# ======================================================
class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenSerializer


class BaseAutoUserViewSet(viewsets.ModelViewSet):
    permission_classes = [ReadOnlyOrAuthenticated]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user.username)

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user.username)


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


# ======================================================
# 🎨 Dashboard + Lists
# ======================================================
def dashboard(request):
    clients = Client.objects.all()
    projects = Project.objects.all()
    members = Member.objects.all()

    clients_status = {label: clients.filter(status=key).count() for key, label in Client.STATUS_CHOICES}
    projects_status = {label: projects.filter(status=key).count() for key, label in Project.STATUS_CHOICES}

    # ✅ Active/Hot members (currently working)
    active_hot_members = Member.objects.filter(
        memberassigned__project__status__in=["active", "hot"],
        memberassigned__is_active=True
    ).distinct()

    current_members = active_hot_members.count()
    past_members = members.exclude(id__in=active_hot_members).count()

    # ✅ Only show HOT projects in MemberAssigned
    hot_assignments = MemberAssigned.objects.select_related("member", "project__client").filter(
        is_active=True,
        project__status="hot"
    )

    member_projects = []
    for assign in hot_assignments:
        project_name = assign.project.name if assign.project else "N/A"
        project_status = assign.project.status.upper() if assign.project and assign.project.status else "N/A"
        client_name = assign.project.client.Client_name if assign.project and assign.project.client else "N/A"

        member_projects.append({
            "id": assign.id,
            "member": assign.member.name if assign.member else "N/A",
            "projects": [f"{project_name} ({project_status})"],
            "clients": [client_name],
        })

    recent_activities = ProjectActivity.objects.select_related(
        "project", "project__client"
    ).order_by("-updated_at")[:10]

    context = {
        "clients_count": clients.count(),
        "clients_status": clients_status,
        "projects_count": projects.count(),
        "projects": projects_status,
        "current_members": current_members,
        "past_members": past_members,
        "member_projects": member_projects,  # Already filtered to only HOT projects
        "recent_activities": recent_activities,
        "is_admin": request.user.is_authenticated and request.user.is_staff
    }
    return render(request, "index.html", context)


def clients_list(request):
    status = request.GET.get("status")
    clients = Client.objects.all()
    if status:
        clients = clients.filter(status=status)
    return render(request, "clients_list.html", {
        "clients": clients,
        "status": status,
        "is_admin": request.user.is_authenticated and request.user.is_staff
    })


def projects_list(request):
    status = request.GET.get("status")
    projects = Project.objects.all()
    if status:
        projects = projects.filter(status=status)
    return render(request, "projects_list.html", {
        "projects": projects,
        "status": status,
        "is_admin": request.user.is_authenticated and request.user.is_staff
    })


def members_list(request):
    status = request.GET.get("status")
    members = Member.objects.all()

    if status == "current":
        members = Member.objects.filter(
            memberassigned__project__status__in=["active", "hot"],
            memberassigned__is_active=True
        ).distinct()
    elif status == "past":
        active_hot_members = Member.objects.filter(
            memberassigned__project__status__in=["active", "hot"],
            memberassigned__is_active=True
        ).distinct()
        members = Member.objects.exclude(id__in=active_hot_members)

    return render(request, "members_list.html", {
        "members": members,
        "status": status,
        "is_admin": request.user.is_authenticated and request.user.is_staff
    })


# ======================================================
# ➕ Add Views (Admin Only)
# ======================================================
@admin_required
def add_client(request):
    if request.method == "POST":
        Client.objects.create(
            Client_name=request.POST["Client_name"],
            status=request.POST["status"],
            created_by=request.user.username
        )
        return redirect("clients_list")
    return render(request, "clients_add.html")


@admin_required
def add_project(request):
    if request.method == "POST":
        client = get_object_or_404(Client, id=request.POST["client"])
        project = Project.objects.create(
            name=request.POST["name"],
            client=client,
            type=request.POST["type"],
            status=request.POST["status"],
            start_date=request.POST.get("start_date") or None,
            end_date=request.POST.get("end_date") or None,
            hosting_provider=request.POST.get("hosting_provider"),
            github_repo=request.POST.get("github_repo"),
            live_url=request.POST.get("live_url"),
            description=request.POST.get("description"),
            created_by=request.user.username
        )

        keys = request.POST.getlist("credentials_key[]")
        values = request.POST.getlist("credentials_value[]")
        for k, v in zip(keys, values):
            if k.strip() and v.strip():
                ProjectCredential.objects.create(
                    project=project,
                    key=k.strip(),
                    value=v.strip(),
                    created_by=request.user.username
                )

        return redirect("projects_list")
    return render(request, "projects_add.html", {"clients": Client.objects.all()})


@admin_required
def add_project_credential(request):
    if request.method == "POST":
        project = get_object_or_404(Project, id=request.POST["project"])
        ProjectCredential.objects.create(
            project=project,
            key=request.POST["key"],
            value=request.POST["value"],
            created_by=request.user.username
        )
        return redirect("projects_list")
    return render(request, "projectcredentials_add.html", {"projects": Project.objects.all()})


@admin_required
def add_team(request):
    if request.method == "POST":
        team = Team.objects.create(
            team_type=request.POST["team_type"],
            created_by=request.user.username
        )
        members = request.POST.getlist("members")
        if members:
            team.members.set(Member.objects.filter(id__in=members))
        return redirect("members_list")
    return render(request, "teams_add.html", {"members": Member.objects.all()})


@admin_required
def add_member(request):
    if request.method == "POST":
        Member.objects.create(
            name=request.POST["name"],
            role=request.POST["role"],
            created_by=request.user.username
        )
        return redirect("members_list")
    return render(request, "members_add.html")


@admin_required
def add_member_assigned(request):
    if request.method == "POST":
        member = get_object_or_404(Member, id=request.POST["member"])
        project = get_object_or_404(Project, id=request.POST["project"])
        MemberAssigned.objects.create(
            member=member,
            project=project,
            assigned_from=request.POST.get("assigned_from") or None,
            assigned_to=request.POST.get("assigned_to") or None,
            is_active="is_active" in request.POST,
            created_by=request.user.username
        )
        return redirect("members_list")
    return render(request, "memberassigned_add.html", {
        "members": Member.objects.all(),
        "projects": Project.objects.filter(status="active")
    })


@admin_required
def add_project_activity(request):
    if request.method == "POST":
        project = get_object_or_404(Project, id=request.POST["project"])
        ProjectActivity.objects.create(
            project=project,
            status=request.POST["status"],
            activity_from=request.POST.get("activity_from") or None,
            activity_to=request.POST.get("activity_to") or None,
            remarks=request.POST.get("remarks"),
            created_by=request.user.username
        )
        return redirect("projects_list")
    return render(request, "projectactivities_add.html", {"projects": Project.objects.all()})


# ======================================================
# ✏️ Update Views (Admin Only)
# ======================================================
@admin_required
def edit_client(request, pk):
    client = get_object_or_404(Client, pk=pk)
    if request.method == "POST":
        client.Client_name = request.POST["Client_name"]
        client.status = request.POST["status"]
        client.updated_by = request.user.username
        client.save()
        return redirect("clients_list")
    return render(request, "client_edit.html", {
        "form": client,
        "status_choices": Client.STATUS_CHOICES
    })


@admin_required
def delete_client(request, pk):
    client = get_object_or_404(Client, pk=pk)
    if request.method == "POST":
        client.delete()
        return redirect("clients_list")
    return render(request, "client_confirm_delete.html", {"object": client})


@admin_required
def edit_project(request, pk):
    project = get_object_or_404(Project, id=pk)
    if request.method == "POST":
        project.name = request.POST.get("name", project.name)
        project.client = get_object_or_404(Client, id=request.POST["client"])
        project.type = request.POST.get("type", project.type)
        project.status = request.POST.get("status", project.status)
        project.start_date = request.POST.get("start_date") or project.start_date
        project.end_date = request.POST.get("end_date") or project.end_date
        project.hosting_provider = request.POST.get("hosting_provider", project.hosting_provider)
        project.github_repo = request.POST.get("github_repo", project.github_repo)
        project.live_url = request.POST.get("live_url", project.live_url)
        project.description = request.POST.get("description", project.description)
        project.updated_by = request.user.username
        project.save()

        ProjectCredential.objects.filter(project=project).delete()
        keys = request.POST.getlist("credentials_key[]")
        values = request.POST.getlist("credentials_value[]")
        for k, v in zip(keys, values):
            if k.strip() and v.strip():
                ProjectCredential.objects.create(
                    project=project,
                    key=k.strip(),
                    value=v.strip(),
                    created_by=request.user.username
                )

        return redirect("projects_list")

    return render(request, "project_edit.html", {
        "project": project,
        "clients": Client.objects.all(),
        "status_choices": Project.STATUS_CHOICES,
        "type_choices": Project.PROJECT_TYPES,
    })


@admin_required
def delete_project(request, pk):
    project = get_object_or_404(Project, pk=pk)
    if request.method == "POST":
        project.delete()
        return redirect("projects_list")
    return render(request, "project_confirm_delete.html", {"object": project})


@admin_required
def edit_member(request, pk):
    member = get_object_or_404(Member, pk=pk)
    if request.method == "POST":
        member.name = request.POST["name"]
        member.role = request.POST["role"]
        member.updated_by = request.user.username
        member.save()
        return redirect("members_list")
    return render(request, "member_edit.html", {"form": member})


@admin_required
def delete_member(request, pk):
    member = get_object_or_404(Member, pk=pk)
    if request.method == "POST":
        member.delete()
        return redirect("members_list")
    return render(request, "member_confirm_delete.html", {"object": member})


@admin_required
def edit_member_assigned(request, pk):
    assignment = get_object_or_404(MemberAssigned, pk=pk)
    if request.method == "POST":
        assignment.member = get_object_or_404(Member, id=request.POST["member"])
        assignment.project = get_object_or_404(Project, id=request.POST["project"])
        assignment.assigned_from = request.POST.get("assigned_from") or assignment.assigned_from
        assignment.assigned_to = request.POST.get("assigned_to") or assignment.assigned_to
        assignment.is_active = "is_active" in request.POST
        assignment.updated_by = request.user.username
        assignment.save()
        return redirect("dashboard")
    return render(request, "memberassigned_edit.html", {
        "assignment": assignment,
        "members": Member.objects.all(),
        "projects": Project.objects.all(),
    })


@admin_required
def delete_member_assigned(request, pk):
    assignment = get_object_or_404(MemberAssigned, pk=pk)
    if request.method == "POST":
        assignment.delete()
        return redirect("dashboard")
    return render(request, "memberassigned_confirm_delete.html", {"object": assignment})


@admin_required
def edit_project_activity(request, pk):
    activity = get_object_or_404(ProjectActivity, pk=pk)
    if request.method == "POST":
        activity.project = get_object_or_404(Project, id=request.POST["project"])
        activity.status = request.POST.get("status", activity.status)
        activity.activity_from = request.POST.get("activity_from") or activity.activity_from
        activity.activity_to = request.POST.get("activity_to") or activity.activity_to
        activity.remarks = request.POST.get("remarks", activity.remarks)
        activity.updated_by = request.user.username
        activity.save()
        return redirect("projects_list")

    return render(request, "projectactivities_edit.html", {
        "activity": activity,
        "projects": Project.objects.all(),
        "status_choices": ProjectActivity.STATUS_CHOICES
    })


@admin_required
def delete_project_activity(request, pk):
    activity = get_object_or_404(ProjectActivity, pk=pk)
    if request.method == "POST":
        activity.delete()
        return redirect("projects_list")
    return render(request, "projectactivities_confirm_delete.html", {"object": activity})


# ======================================================
# 🔐 Auth Views
# ======================================================
def login_view(request):
    """Custom login page"""
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("dashboard")
        else:
            return render(request, "login.html", {"error": "Invalid username or password"})
    return render(request, "login.html")


def logout_view(request):
    """Logout and redirect to login page"""
    logout(request)
    return redirect("login")
