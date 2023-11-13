from django.shortcuts import render


def test_registration_api_page(request):
    return render(request, 'test.html')