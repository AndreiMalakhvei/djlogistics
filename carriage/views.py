from django.shortcuts import render
from carriage.models import Test

def test(request):
    test_var = Test.objects.get(pk=1)
    return render(request, 'carriage/index.html', {'test_var': test_var})

def carriage_main(request):
    pass
