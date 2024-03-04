from django.shortcuts import render
from django.template import RequestContext

def index(request):
    
    if request.method == 'POST':
        if request.FILES['audio_file'] != None:
            uploaded_file = request.FILES['audio_file']
            # Do something with the uploaded file
        return render(request, 'index1.html')
    else:
        return render(request, 'index1.html')
    # if request.user.is_authenticated:
    #     return render(request, 'index1.html')
    # else:
    #     return render(request, 'index1.html')


    
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

def login(request):
    return render(request, 'login.html')

def register(request):
    return render(request, 'register.html')

def terms_conditions(request):
    return render(request, 'terms_conditions.html')

def privacy_policy(request):
    return render(request, 'privacy_policy.html')

def pricing(request):
    return render(request, 'pricing.html')