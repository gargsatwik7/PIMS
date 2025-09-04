from django.contrib import admin
from django.urls import path, include
from core import views

urlpatterns = [
    path('admin/', admin.site.urls),

    # =============================
    # HTML Pages (Dashboard + Lists)
    # =============================
    path('', views.dashboard, name='dashboard'),  # Home/Dashboard
    path('clients/', views.clients_list, name='clients_list'),
    path('projects/', views.projects_list, name='projects_list'),
    path('members/', views.members_list, name='members_list'),

    # =============================
    # Add Pages (Admin Only)
    # =============================
    path('clients/add/', views.add_client, name='add_client'),
    path('projects/add/', views.add_project, name='add_project'),
    path('credentials/add/', views.add_project_credential, name='add_project_credential'),
    path('teams/add/', views.add_team, name='add_team'),
    path('members/add/', views.add_member, name='add_member'),
    path('memberassigned/add/', views.add_member_assigned, name='add_member_assigned'),
    path('activities/add/', views.add_project_activity, name='add_project_activity'),

    # =============================
    # Edit / Delete Pages (Admin Only)
    # =============================
    # Clients
    path('clients/<int:pk>/edit/', views.edit_client, name='edit_client'),
    path('clients/<int:pk>/delete/', views.delete_client, name='delete_client'),

    # Projects
    path('projects/<int:pk>/edit/', views.edit_project, name='edit_project'),
    path('projects/<int:pk>/delete/', views.delete_project, name='delete_project'),

    # Members
    path('members/<int:pk>/edit/', views.edit_member, name='edit_member'),
    path('members/<int:pk>/delete/', views.delete_member, name='delete_member'),

    # Member Assigned
    path('memberassigned/<int:pk>/edit/', views.edit_member_assigned, name='edit_member_assigned'),
    path('memberassigned/<int:pk>/delete/', views.delete_member_assigned, name='delete_member_assigned'),

    # Project Activities
    path('activities/<int:pk>/edit/', views.edit_project_activity, name='edit_project_activity'),
    path('activities/<int:pk>/delete/', views.delete_project_activity, name='delete_project_activity'),

    # =============================
    # Auth Pages
    # =============================
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # =============================
    # API URLs
    # =============================
    path('api/', include('core.urls')),
]
