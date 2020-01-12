from django.shortcuts import render
from .models import Workshop

def index(request):
    workshops = Workshop.objects.filter(open=True)
    return render(request, 'index.html', {'workshops':workshops})
