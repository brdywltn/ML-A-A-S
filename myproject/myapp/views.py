# views.py
import os
from django.contrib.auth import login
from django.contrib import messages
from django.shortcuts import render, redirect
import logging
import json

from .forms import InstrumentDetectionForm
from .models import Action, UserTokenCount, Profile, ModelConfig, ModelPerformanceMetrics

# Django Rest Framework imports
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import InstrumentDetectionSerializer
from .audio_preprocessing import preprocess_audio_for_inference
import requests

# Authentication Imports
from django.urls import reverse_lazy
from django.views import View, generic
from .models import Profile, ModelConfig
from .forms import UserRegisterForm, LoginAuthenticationForm
from django.contrib.auth.views import LoginView

from django.contrib.auth.mixins import UserPassesTestMixin
from django.views.generic import TemplateView

import re

from .utils import get_log_data, create_log

logger = logging.getLogger(__name__)

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
def terms_conditions(request):
    return render(request, 'terms_conditions.html')

def privacy_policy(request):
    return render(request, 'privacy_policy.html')

def pricing(request):
    return render(request, 'pricing.html')

def submit_feedback(request):
    if request.method == 'POST' and request.user.is_authenticated:
        prediction = request.POST.get('prediction')
        liked = request.POST.get('feedback') == 'true'
        file_name = request.POST.get('file_name')  # Get the filename from the form data
        
        # Create log data using the get_log_data function
        log_data = get_log_data(
            user=request.user,
            action=Action.FEEDBACK_SUBMITTED,
            status='success',
            file=file_name,  # Use the filename obtained from the form
            description=prediction,
            feedback=liked
        )
        
        # Create the Log entry using the create_log function
        create_log(request.user, log_data)
        
        return redirect('index')
    else:
        messages.error(request, 'Invalid request')
        return redirect('index')


def index(request):
    # Initialize default context
    context = {'form': InstrumentDetectionForm(), 'predictions': [], 'file_name': None}

    # Handle authenticated users
    if request.user.is_authenticated:
        token_count = UserTokenCount.objects.get(user=request.user).token_count
        context['token_count'] = token_count

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

                    if request.user.is_authenticated:
                        feedback = request.POST.get('feedback')  # Get the user's feedback from the form
                        predictions_string = ', '.join(response.data['predictions'])
                        log_data = get_log_data(request.user, Action.RUN_ALGORITHM, 'success', file=uploaded_file.name, 
                                                description=predictions_string, feedback=feedback)
                        create_log(request.user, log_data)
            else:
                context['form'] = form
    else:
        if request.method == 'POST':
            # Assuming you want to do something specific with the file if it's uploaded
            uploaded_file = request.FILES.get('audio_file')
            if uploaded_file:
                # Process the uploaded file as needed
                pass

    # For GET requests or if form is not valid, render the page with the default or updated context
    if request.user.is_authenticated:
        return render(request, 'index1.html', context)
    else:
        return render(request, 'index2.html')



# Authentication
class RegisterView(generic.CreateView):
    form_class = UserRegisterForm
    success_url = reverse_lazy('index')
    template_name = 'registration/register.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            messages.info(request, 'You are already logged in.')
            return redirect('index')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        response = super().form_valid(form)
        user = self.object  # Grab the user instance

        # Ensure the user is active; this line might be redundant if you're sure users are active by default
        user.is_active = True
        user.save()

        # Check if the Profile exists, and if not, create it
        if not Profile.objects.filter(user=user).exists():
            Profile.objects.create(user=user, user_type=0)  # Default user type as Basic User

        # Log the user in
        login(self.request, user)

        return response


class CustomLoginView(LoginView):
    authentication_form = LoginAuthenticationForm
    template_name = 'registration/login.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            messages.info(request, 'You are already logged in.')
            return redirect('index')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        # Create log if user is authenticated
        login(self.request, form.get_user())

        log_data = get_log_data(form.get_user(), Action.LOGIN, 'success')
        create_log(form.get_user(), log_data)

        return super().form_valid(form)




# Model Views
class InstrumentDetectionView(APIView):

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_anonymous:
            messages.info(request, 'Must be logged in as a user to access this page.')
            return redirect('login')
        else:
            user_token_count = UserTokenCount.objects.get(user=request.user)
        if user_token_count.token_count < 1:
            messages.info(request, 'You do not have enough tokens to make a prediction.')
            return redirect('pricing')
        # Add a check for the existence of files in the request.FILES dictionary
        elif 'audio_file' not in request.FILES:
            messages.info(request, 'No audio file was uploaded.')
            return redirect('index')
        else: return super().dispatch(request, *args, **kwargs)
    
    def post(self, request):
        try:
            model_config = ModelConfig.load()
            selected_model_version = model_config.selected_model_version
            # Get the user's token count
            user_token_count = UserTokenCount.objects.get(user=request.user)

            # Decrease the user's token count by one
            user_token_count.token_count -= 1
            user_token_count.save()

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
                # url = 'http://tensorflow_serving:8501/v1/models/instrument_model/versions/2:predict'
                url = f'http://tensorflow_serving:8501/v1/models/instrument_model/versions/{selected_model_version}:predict'
                headers = {"Content-Type": "application/json"}
                response = requests.post(url, data=data, headers=headers)

                # Process the response
                if response.status_code == 200:
                    print('Predictions received')
                    raw_predictions = response.json()['predictions']
                    # Convert raw prediction numbers into percentages
                    formatted_predictions = self.format_predictions(raw_predictions)
                    return Response({"predictions": formatted_predictions}, status=status.HTTP_200_OK)
                else:
                    return Response({"error": "Failed to get predictions"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        except Exception as e:
            logger.error(f"An error occurred: {e}")
            messages.error(request, 'An error occurred: {e}')
            return redirect('index')


    def format_predictions(self, predictions):
        instruments = ['Guitar', 'Drum', 'Violin', 'Piano']
        instrument_windows = {instrument: [] for instrument in instruments}

        for window_index, prediction in enumerate(predictions, start=1):
            highest_score_index = prediction.index(max(prediction))
            highest_score_instrument = instruments[highest_score_index]
            instrument_windows[highest_score_instrument].append(window_index)

        formatted_predictions = []
        for instrument, windows in instrument_windows.items():
            if windows:
                window_list = ', '.join(map(str, windows))
                formatted_predictions.append(f"{instrument} - Windows: {window_list}")

        return formatted_predictions
    



class ModelPerformanceView(UserPassesTestMixin, TemplateView):
    template_name = 'model_performance.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_anonymous:
            messages.info(request, 'Must be logged in as an ML Engineer or Superuser to access this page.')
            return redirect('login')
        elif request.user.profile.user_type != 2 and not request.user.is_superuser:
            messages.info(request, 'Must be logged in as an ML Engineer or Superuser to access this page.')
            return redirect('users')
        else:
            return super().dispatch(request, *args, **kwargs)

    def test_func(self):
        return self.request.user.is_authenticated and (self.request.user.is_superuser or self.request.user.profile.user_type == 2)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        metrics_url = 'http://tensorflow_serving:8501/monitoring/prometheus/metrics'
        response = requests.get(metrics_url)

        if response.status_code == 200:
            metrics_data = response.text

            # Extract metrics using regular expressions
            request_count = re.search(r':tensorflow:serving:request_count{model_name="instrument_model",status="OK"} (\d+)', metrics_data)
            request_latency_sum = re.search(r':tensorflow:serving:request_latency_sum{model_name="instrument_model",API="predict",entrypoint="REST"} ([\d\.e\+]+)', metrics_data)
            request_latency_count = re.search(r':tensorflow:serving:request_latency_count{model_name="instrument_model",API="predict",entrypoint="REST"} (\d+)', metrics_data)
            runtime_latency_sum = re.search(r':tensorflow:serving:runtime_latency_sum{model_name="instrument_model",API="Predict",runtime="TF1"} ([\d\.e\+]+)', metrics_data)
            runtime_latency_count = re.search(r':tensorflow:serving:runtime_latency_count{model_name="instrument_model",API="Predict",runtime="TF1"} (\d+)', metrics_data)
            model_load_latency = re.search(r':tensorflow:cc:saved_model:load_latency{model_path="/models/instrument_model/2"} (\d+)', metrics_data)

            # Get or create the ModelPerformanceMetrics instance
            metrics, _ = ModelPerformanceMetrics.objects.get_or_create(pk=1)

            # Update the metrics in the database
            metrics.request_count = int(request_count.group(1)) if request_count else 0
            metrics.request_latency_sum = float(request_latency_sum.group(1)) if request_latency_sum else 0
            metrics.request_latency_count = int(request_latency_count.group(1)) if request_latency_count else 0
            metrics.runtime_latency_sum = float(runtime_latency_sum.group(1)) if runtime_latency_sum else 0
            metrics.runtime_latency_count = int(runtime_latency_count.group(1)) if runtime_latency_count else 0
            metrics.model_load_latency = float(model_load_latency.group(1)) if model_load_latency else 0
            metrics.save()

            # Calculate average latencies in seconds
            avg_request_latency = metrics.request_latency_sum / metrics.request_latency_count / 1e6 if metrics.request_latency_count else None
            avg_runtime_latency = metrics.runtime_latency_sum / metrics.runtime_latency_count / 1e6 if metrics.runtime_latency_count else None

            context['metrics'] = {
                'request_count': metrics.request_count,
                'avg_request_latency': avg_request_latency,
                'avg_runtime_latency': avg_runtime_latency,
                'model_load_latency': metrics.model_load_latency / 1e6
            }
        else:
            context['metrics'] = None

        return context
    def post(self, request, *args, **kwargs):
        if 'reset_metrics' in request.POST:
            metrics = ModelPerformanceMetrics.objects.get(pk=1)
            metrics.reset_metrics()
            metrics.save()
            return redirect('users')
        else:
            messages.error(request, 'Invalid request')
            return redirect('users')

class ModelSelectionView(UserPassesTestMixin, View):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_anonymous:
            messages.info(request, 'Must be logged in as an ML Engineer or Superuser to access this page.')
            return redirect('login')
        elif request.user.profile.user_type != 2 and not request.user.is_superuser:
            messages.info(request, 'Must be logged in as an ML Engineer or Superuser to access this page.')
            return redirect('users')
        else:
            return super().dispatch(request, *args, **kwargs)

    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.profile.user_type == 2

    def get(self, request):
        model_versions = os.listdir('models/instrument_model')
        model_config = ModelConfig.load()
        context = {
            'model_versions': model_versions,
            'selected_model_version': model_config.selected_model_version,
        }
        return render(request, 'model_selection.html', context)

    def post(self, request):
        selected_model_version = request.POST.get('model_version')
        model_config = ModelConfig.load()
        model_config.selected_model_version = selected_model_version
        model_config.save()
        messages.success(request, f'Selected model version: {selected_model_version}')
        return redirect('users')
    



