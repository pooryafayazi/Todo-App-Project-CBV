from django_filters import FilterSet, AllValuesFilter
from django_filters import DateTimeFilter, NumberFilter
from tasks.models import Task
from django_filters import DateFromToRangeFilter
from datetime import datetime
import pytz
import django_filters


class TaskFilter(FilterSet):
    now = str(datetime.now(pytz.utc))[:19]
    due_date_min = DateTimeFilter(field_name='due_date', lookup_expr='gte', label=f'Now is {now}, Due Date from')
    due_date_max = DateTimeFilter(field_name='due_date', lookup_expr='lte', label=f'Now is {now}, Due Date to')
    # created_date_min = DateTimeFilter(field_name='created_date', lookup_expr='gte', label=f'Now is {now}, created Date from')
    # created_date_max = DateTimeFilter(field_name='created_date', lookup_expr='lte', label=f'Now is {now}, created Date to')
    release_year = django_filters.NumberFilter(field_name='created_date', lookup_expr='year')
    release_month = django_filters.NumberFilter(field_name='created_date', lookup_expr='month')
    release_day = django_filters.NumberFilter(field_name='created_date', lookup_expr='day')

    # due_date = DateFromToRangeFilter(field_name='due_date',label=f'{now} is Due Date format')
    created_date = DateFromToRangeFilter(field_name='created_date',label=f'{now} is created Date format')
    creator = AllValuesFilter(field_name='creator')
    complete = AllValuesFilter(field_name='complete')
    active = AllValuesFilter(field_name='active')
    class Meta:
        model = Task
        fields = ['creator','complete','active','release_year','release_month','release_day','due_date_min','due_date_max']
        # fields = ['creator','complete','active','due_date','created_date']