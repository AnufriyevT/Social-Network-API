from django_filters import rest_framework as filters

from core.models import Like


class LikeFilterSet(filters.FilterSet):
    # was made custom filter fields to filter only by date (not datetime)
    pub_date__lte = filters.DateFilter(field_name="pub_date", lookup_expr="lte")
    pub_date__gte = filters.DateFilter(field_name="pub_date", lookup_expr="gte")
    pub_date = filters.DateFilter(lookup_expr="date")

    class Meta:
        model = Like
        fields = ("pub_date__lte", "pub_date__gte", "pub_date")
