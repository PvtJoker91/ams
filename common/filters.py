from django_filters import rest_framework as filters
from rest_framework.exceptions import ParseError


class CustomFilter(filters.DjangoFilterBackend):
    def filter_queryset(self, request, queryset, view):
        limit = request.query_params.get('limit', None)
        if limit is not None:
            try:
                limit = int(limit)
                if limit <= 0:
                    raise ValueError("Limit should be a positive integer")
            except ValueError:
                raise ParseError("Invalid limit parameter. It should be a positive integer.")

            filtered = super().filter_queryset(request, queryset, view)
            if filtered.count() > limit:
                raise ParseError(f"Превышен лимит выдачи в {limit} записей! Измените условия поиска.")
        return super().filter_queryset(request, queryset, view)
