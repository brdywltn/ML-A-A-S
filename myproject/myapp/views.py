from django.shortcuts import render
from django.template import RequestContext
import logging
from django.http import HttpResponse
from django.utils import timezone
from .models import Log, Action

logger = logging.getLogger(__name__)

def get_log_data(action, status='success', file=None, **additional_fields):
    log_data = {
        'action': action.value,
        'status': status,
        'file': file,
    }
    log_data.update(additional_fields)
    return log_data

def create_log(user, log_data):
    Log.objects.create(user=user, log=log_data)

def handling_music_file(request):
    if request.method == 'POST':
        if 'audio_file' in request.FILES:
            log_data = {
                'action': 'File uploaded',
                'file': request.FILES['audio_file'].name,
            }
            log_data = get_log_data(Action.UPLOAD_FILE, 'success', file=request.FILES['audio_file'].name)
            # create_log(request.user if request.user.is_authenticated else None, log_data)
            return HttpResponse('File uploaded successfully!',log_data)
    log_data = get_log_data(Action.invalid_file, 'error')
    # create_log(None, log_data)
    return HttpResponse('File invalid',log_data)

def index(request):
    #for now this authenication just returns the main view
    #when user auth is done change the else to return index2.html
    if request.user.is_authenticated:
        if request.method == 'POST':
            if request.FILES['audio_file'] != None:
                uploaded_file = request.FILES['audio_file']
                # Do something with the uploaded file
            return render(request, 'index1.html')
        else:
            return render(request, 'index1.html')
    else:
        return render(request, 'index1.html')

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

#For testing the receipts ONLY. TODO: delete when working
def generate_pdf(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="example.pdf"'

    p = canvas.Canvas(response)
    p.drawString(100, 800, "Hello, this is a PDF!")
    p.showPage()
    p.save()

    return response


#For testing the receipts ONLY. TODO: delete when working
def generate_pdf(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="example.pdf"'

    p = canvas.Canvas(response)
    p.drawString(100, 800, "Hello, this is a PDF!")
    p.showPage()
    p.save()

    return response