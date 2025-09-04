from django.db import models


# ------------------ CLIENT ------------------
class Client(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('hot', 'Hot'),
    ]
    
    Client_name = models.CharField(max_length=100, default="Unknown Client")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    created_by = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.CharField(max_length=100, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return self.Client_name


# ------------------ PROJECT ------------------
class Project(models.Model):
    PROJECT_TYPES = [
        ('internal', 'Internal'),
        ('client', 'Client'),
        ('freelance', 'Freelance'),
    ]
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('hot', 'Hot'),
        ('dead', 'Dead'),
    ]

    name = models.CharField(max_length=100)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    type = models.CharField(max_length=50, choices=PROJECT_TYPES)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, null=True, blank=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    hosting_provider = models.CharField(max_length=100, null=True, blank=True)
    github_repo = models.URLField(blank=True, null=True)
    live_url = models.URLField(blank=True, null=True)
    description = models.TextField(null=True, blank=True) 
    teams_assigned = models.ManyToManyField('Team', blank=True)
    created_by = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.CharField(max_length=100, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return self.name


# ------------------ PROJECT CREDENTIAL ------------------
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


# ------------------ TEAM ------------------
class Team(models.Model):
    team_type = models.CharField(max_length=50)
    members = models.ManyToManyField('Member', blank=True)
    created_by = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.CharField(max_length=100, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return self.team_type


# ------------------ MEMBER ------------------
class Member(models.Model):
    # STATUS_CHOICES = [
    #     ('current', 'Currently Working'),
    #     ('past', 'Ex Employee'),
    # ]
    name = models.CharField(max_length=100)
    role = models.CharField(max_length=50)
    # status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='current')
    projects = models.ManyToManyField(Project, through='MemberAssigned', related_name='members')
    created_by = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.CharField(max_length=100, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return self.name


# ------------------ MEMBER ASSIGNED ------------------
class MemberAssigned(models.Model):
    member = models.ForeignKey('Member', on_delete=models.CASCADE)
    project = models.ForeignKey('Project', on_delete=models.CASCADE)
    assigned_from = models.DateField(null=True, blank=True)
    assigned_to = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_by = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.CharField(max_length=100, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return f"{self.member.name}  {self.project.name} ({'Active' if self.is_active else 'Inactive'})"


# ------------------ PROJECT ACTIVITY ------------------
class ProjectActivity(models.Model):
    STATUS_CHOICES = [
        ('started', 'Started'),
        ('paused', 'Paused'),
        ('resumed', 'Resumed'),
        ('completed', 'Completed'),
        ('on-hold', 'On Hold'),
    ]

    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='activity_logs')
    activity_from = models.DateField(null=True, blank=True)
    activity_to = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, null=True, blank=True)
    remarks = models.TextField(blank=True, null=True)
    created_by = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.CharField(max_length=100, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return f"{self.project.name}  {self.status} ({self.activity_from} to {self.activity_to})"
