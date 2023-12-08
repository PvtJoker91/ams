
from django.http import JsonResponse

from rest_framework.decorators import api_view


@api_view(['GET'])
def me(request):
    if not request.user.is_anonymous:
        return JsonResponse({
            'id': request.user.id,
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
            'email': request.user.email,
    })
    else:
        raise TypeError('No data for anonymous user')


