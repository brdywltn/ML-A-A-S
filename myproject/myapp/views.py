from django.shortcuts import render
from django.template import RequestContext

def index(request):
    return render(request, 'index.html')

def users(request):
    return render(request, 'user_page.html')

def handler404(request, *args, **kwargs):
    response = render(request, '404.html', {})
    response.status_code = 404
    return response

def handler500(request, *args, **kwargs):
    response = render(request, '500.html', {})
    response.status_code = 500
    return response

def maintenance(request):
    return render(request, 'maintenance.html')