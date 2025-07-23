# from django_filters import rest_framework as filters
# from .models import Project

# class ProjectFilter(filters.FilterSet):
#     start_date = filters.DateFilter(field_name='start_date', lookup_expr='gte')
#     end_date = filters.DateFilter(field_name='end_date', lookup_expr='lte')
#     status = filters.CharFilter(field_name='status', lookup_expr='iexact')
#     type = filters.CharFilter(field_name='type', lookup_expr='iexact')

#     class Meta:
#         model = Project
#         fields = ['status', 'type', 'start_date', 'end_date']


from django_filters import rest_framework as filters
from .models import Project

class ProjectFilter(filters.FilterSet):
    start_year = filters.NumberFilter(field_name='start_date', lookup_expr='year')
    client = filters.CharFilter(field_name='client__Client_name', lookup_expr='icontains')
    type = filters.ChoiceFilter(choices=Project.PROJECT_TYPES)
    status = filters.ChoiceFilter(choices=Project.STATUS_CHOICES)
    start_date = filters.DateFilter(field_name='start_date', lookup_expr='gte')
    end_date = filters.DateFilter(field_name='end_date', lookup_expr='lte')
    hosting = filters.CharFilter(field_name='hosting_provider', lookup_expr='icontains')
    github = filters.BooleanFilter(method='filter_github')
    deployed = filters.BooleanFilter(method='filter_deployed')

    class Meta:
        model = Project
        fields = []

    def filter_github(self, qs, name, val):
        return qs.exclude(github_repo__isnull=True, github_repo__exact='') if val else qs.filter(github_repo__isnull=True) | qs.filter(github_repo__exact='')

    def filter_deployed(self, qs, name, val):
        return qs.exclude(live_url__isnull=True, live_url__exact='') if val else qs.filter(live_url__isnull=True) | qs.filter(live_url__exact='')
