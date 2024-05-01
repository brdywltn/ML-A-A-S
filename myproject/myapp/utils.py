# utils.py
from .models import Log
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Action
import json

def get_log_data(user, action, status='success', file=None, description=None, feedback=None):
    log_data = {
        'username': user.username,
        'action': action.value.format(username=user.username),
        'status': status,
        'file': file,
        'description': description,
        'feedback': feedback,  # Add the feedback field
    }
    return log_data

def create_log(user, log_data):
    Log.objects.create(user=user, log=log_data, feedback=log_data.get('feedback'))

def user_has_credits():
    has_credits = False
    return has_credits

@csrf_exempt
def log_fileupload(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        status = data.get('status')
        file = data.get('file')

        if request.user.is_authenticated:
            log_data = get_log_data(request.user, Action.UPLOAD_FILE, status, file)
            create_log(request.user, log_data)

        return JsonResponse({'message': 'Log created successfully'}, status=201)

    return JsonResponse({'error': 'Invalid request'}, status=400)
