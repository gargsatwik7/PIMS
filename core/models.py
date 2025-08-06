from django.db import models


class Client(models.Model):
    # company_name = models.CharField(max_length=100)
    Client_name = models.CharField(max_length=100, default="Unknown Client")
    created_by = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.CharField(max_length=100, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return self.Client_name 


class Project(models.Model):
    PROJECT_TYPES = [
        ('internal', 'Internal'),
        ('client', 'Client'),
        ('freelance', 'Freelance'),
    ]
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('archived', 'Archived'),
        ('dead', 'Dead'),
    ]

    name = models.CharField(max_length=100)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    type = models.CharField(max_length=50, choices=PROJECT_TYPES)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    hosting_provider = models.CharField(max_length=100)
    github_repo = models.URLField(blank=True, null=True)
    live_url = models.URLField(blank=True, null=True)
    teams_assigned = models.ManyToManyField('Team', blank=True)
    created_by = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.CharField(max_length=100, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return self.name


class ProjectCredential(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='credentials')
    key = models.CharField(max_length=100) 
    value = models.TextField() 
    created_by = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.CharField(max_length=100, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return f"{self.project.name} - {self.key}"


class Team(models.Model):
    # team_name = models.CharField(max_length=100)
    team_type = models.CharField(max_length=50)
    members = models.ManyToManyField('Member', blank=True)
    created_by = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.CharField(max_length=100, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return self.team_type


class Member(models.Model):
    name = models.CharField(max_length=100)
    role = models.CharField(max_length=50)
    projects = models.ManyToManyField(Project, through='MemberAssigned', related_name='members')
    created_by = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.CharField(max_length=100, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return self.name


from django.db import models

class MemberAssigned(models.Model):
    member = models.ForeignKey('Member', on_delete=models.CASCADE)
    project = models.ForeignKey('Project', on_delete=models.CASCADE)
    assigned_from = models.DateField()
    assigned_to = models.DateField()
    is_active = models.BooleanField(default=True)
    created_by = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.CharField(max_length=100, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return f"{self.member.name}  {self.project.name} ({'Active' if self.is_active else 'Inactive'})"

class ProjectActivity(models.Model):
    STATUS_CHOICES = [
        ('started', 'Started'),
        ('paused', 'Paused'),
        ('resumed', 'Resumed'),
        ('completed', 'Completed'),
        ('on-hold', 'On Hold'),
    ]

    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='activity_logs')
    activity_from = models.DateField()
    activity_to = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    remarks = models.TextField(blank=True, null=True)
    created_by = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.CharField(max_length=100, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return f"{self.project.name}  {self.status} ({self.activity_from} to {self.activity_to})"
