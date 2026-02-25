from django_filters import rest_framework as filters
from core.models import Task, Tag


class TaskFilter(filters.FilterSet):
    """Filtros para o modelo Task"""
    title = filters.CharFilter(field_name='title', lookup_expr='icontains')
    status = filters.ChoiceFilter(
        choices=Task.STATUS_CHOICES,
        field_name='status'
    )
    priority = filters.NumberFilter(field_name='priority')
    priority_gte = filters.NumberFilter(field_name='priority', lookup_expr='gte')
    priority_lte = filters.NumberFilter(field_name='priority', lookup_expr='lte')
    tags = filters.ModelMultipleChoiceFilter(
        queryset=Tag.objects.all(),
        field_name='tags',
        to_field_name='id'
    )
    created_after = filters.DateTimeFilter(field_name='created_at', lookup_expr='gte')
    created_before = filters.DateTimeFilter(field_name='created_at', lookup_expr='lte')

    class Meta:
        model = Task
        fields = ['title', 'status', 'priority', 'tags', 'created_after', 'created_before']


class TagFilter(filters.FilterSet):
    """Filtros para o modelo Tag"""
    name = filters.CharFilter(field_name='name', lookup_expr='icontains')

    class Meta:
        model = Tag
        fields = ['name']