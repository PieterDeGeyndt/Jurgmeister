from django.shortcuts import render,get_object_or_404
from .models import Services

def allservices(request):
    services = Services.objects
    return render(request,'services/allservices.html',{'services': services})

def servicedetail(request, about_id):
    detailservice = get_object_or_404(Services, pk=service_id)
    return render(request,'services/detail.html', {'service': detailservice})