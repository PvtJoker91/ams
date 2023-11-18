from django.shortcuts import render


def test_reg(request):
    return render(request, 'test.html')