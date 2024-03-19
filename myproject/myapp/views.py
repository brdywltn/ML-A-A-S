from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import HttpResponse
from django.utils import timezone
from django.shortcuts import render, redirect
from django.template import RequestContext
import logging
from reportlab.pdfgen import canvas
import json
from datetime import datetime

from .forms import InstrumentDetectionForm, CustomRegistrationForm, LoginForm
from .models import Log, Action, User
from django.http import JsonResponse
from django.db import connection

# Django Rest Framework imports
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import InstrumentDetectionSerializer
from .audio_preprocessing import preprocess_audio_for_inference
import requests

logger = logging.getLogger(__name__)

def get_log_data(action, status='success', file=None, description=None):
    log_data = {
        'action': action.value,
        'status': status,
        'file': file,
        'description': description,
    }
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
            create_log(request.user if request.user.is_authenticated else None, log_data)
            return HttpResponse('File uploaded successfully!',log_data)
    log_data = get_log_data(Action.invalid_file, 'error')
    create_log(None, log_data)
    return HttpResponse('File invalid',log_data)

def admin_table(request):
    # Execute the query and fetch all rows
    query = """SELECT date, user, log FROM myapp_log ORDER BY date DESC"""
    with connection.cursor() as cursor:
        cursor.execute(query)
        rows = cursor.fetchall()

    # Create a list of dictionaries from the query results
    data = []
    for row in rows:
        # Parse the JSON string into a dictionary
        log = json.loads(row[2])
        # Create a dictionary with the date, user, and JSON fields
        date = row[0].strftime('%Y-%m-%d %H:%M:%S')
        entry = {'date': date, 'user': row[1], 'file': log['file'], 'action': log['action'], 'status': log['status']}
        data.append(entry)

    # Return the data as a JSON response
    return JsonResponse({'data': data}, safe=False)


def user_table(request):
    # Execute the query and fetch all rows
    query = """SELECT date, user, log FROM myapp_log ORDER BY date DESC"""
    # Only display user logs code below
    # query = """SELECT date, user, log FROM myapp_log WHERE user = '{}' ORDER BY date DESC""".format(request.user)
    with connection.cursor() as cursor:
        cursor.execute(query)
        rows = cursor.fetchall()

    # Create a list of dictionaries from the query results
    data = []
    for row in rows:
        # Parse the JSON string into a dictionary
        log = json.loads(row[2])
        # Create a dictionary with the date, user, and JSON fields
        date = row[0].strftime('%Y-%m-%d %H:%M:%S')
        entry = {'date': date, 'user': row[1], 'file': log['file'], 'action': log['action'], 'status': log['status']}
        data.append(entry)

    # Return the data as a JSON response
    return JsonResponse({'data': data}, safe=False)

def index(request):
    # Initialize default context
    context = {'form': InstrumentDetectionForm(), 
               'predictions': [],
               'file_name': None
               }
    
    # Handle authenticated users
    if request.user.is_authenticated:
        if request.method == 'POST':
            # Assuming you want to do something specific with the file if it's uploaded
            uploaded_file = request.FILES.get('audio_file')
            if uploaded_file:
                # Process the uploaded file as needed
                pass
            # For now, just render the main page again, potentially after handling the uploaded file
        # For GET requests or if POST doesn't involve a file, just show the main page
        return render(request, 'index1.html')

    # Handle unauthenticated users
    else:
        if request.method == 'POST':
            form = InstrumentDetectionForm(request.POST, request.FILES)
            if form.is_valid() and 'audio_file' in request.FILES:
                uploaded_file = request.FILES['audio_file']
                context['file_name'] = uploaded_file.name
                # Make a request to the InstrumentDetectionView to get the predictions
                view = InstrumentDetectionView().as_view()
                response = view(request)
                # Ensure there's a response and it contains predictions before updating context
                if response and hasattr(response, 'data') and 'predictions' in response.data:
                    context['predictions'] = response.data['predictions']
            else:
                context['form'] = form
        # For GET requests or if form is not valid, render the page with the default or updated context
        return render(request, 'index1.html', context)


def users(request):
    # Make a request to the admin_table view to get the data
    context = {}
    data_admin = admin_table(request)
    data_user = user_table(request)
    admin_dict = json.loads(data_admin.content)
    user_dict = json.loads(data_user.content)
    # Pass the data as a context variable to the template
    # !!! ADMIN DATA ONLY DISPLAYED AND GET IF USER IS ADMIN !!!
    context['admin_data'] = admin_dict['data']
    context['user_data'] = user_dict['data']

    return render(request, 'user_page.html', context)

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

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            user = authenticate(request, username=username, password=password)  # Passing request along with username and password

            if user:
                login(request, user=user)  # Passing request along with user
                return redirect('users')
            else:
                messages.error(request, 'Invalid username or password.')
        else:
            pass

    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})


def register(request):
    if request.method == 'POST':
        form = CustomRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('user_login')
    else:
        form = CustomRegistrationForm()

    return render(request, 'register.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect('user_login')

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

# Running the audio file through the model
class InstrumentDetectionView(APIView):
    def post(self, request):
        serializer = InstrumentDetectionSerializer(data=request.data)
        if serializer.is_valid():
            audio_file = serializer.validated_data['audio_file']
            
            # Save the uploaded file temporarily
            # with open('temp_audio.wav', 'wb') as f:
            #     f.write(audio_file.read())
            
            # Preprocess the audio file
            preprocessed_data = preprocess_audio_for_inference(audio_file)
            
            # Prepare data for TensorFlow Serving
            data = json.dumps({"signature_name": "serving_default", "instances": [window.tolist() for window in preprocessed_data]})
            
            # Send request to TensorFlow Serving
            url = 'http://tensorflow_serving:8501/v1/models/instrument_model/versions/2:predict'
            headers = {"Content-Type": "application/json"}
            response = requests.post(url, data=data, headers=headers)
            
            # Process the response
            if response.status_code == 200:
                raw_predictions = response.json()['predictions']
                # Convert raw prediction numbers into percentages
                formatted_predictions = self.format_predictions(raw_predictions)
                return Response({"predictions": formatted_predictions}, status=status.HTTP_200_OK)
            else:
                return Response({"error": "Failed to get predictions"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def convert_to_percentages(self, predictions):
        # Assuming predictions is a list of lists
        percentage_predictions = []
        for prediction in predictions:
            total = sum(prediction)
            # Convert each number to a percentage of the total, rounded to 2 decimal places
            percentages = [round((number / total) * 100, 2) for number in prediction]
            percentage_predictions.append(percentages)
        return percentage_predictions
    
    def format_predictions(self, predictions):
        instruments = ['Guitar', 'Drum', 'Violin', 'Piano']
        formatted_predictions = []
        for window_index, prediction in enumerate(predictions, start=1):
            formatted_window = f"<strong>Window {window_index}</strong><br>"
            formatted_scores = "<br>".join([f"{instruments[i]} - {score:.2f}" for i, score in enumerate(prediction)])
            formatted_predictions.append(f"{formatted_window}{formatted_scores}")
        return formatted_predictions
