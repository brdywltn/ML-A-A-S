# user_views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.db import connection
from django.contrib import messages
from .models import Profile, UserTokenCount
import json

from .decorators import admin_required, ml_engineer_required, accountant_required, login_required, admin_accountant_required, \
    admin_ml_engineer_required
from .models import Action
from .utils import get_log_data, create_log


@login_required
@admin_ml_engineer_required
def admin_table(request):

    query = """SELECT date, log, user_id, feedback FROM myapp_log ORDER BY date DESC"""
    with connection.cursor() as cursor:
        cursor.execute(query)
        rows = cursor.fetchall()

    # Create a list of dictionaries from the query results
    data = []
    for row in rows:
        # Parse the JSON string into a dictionary
        log = json.loads(row[1])
        # Get the user object based on the user_id
        user_id = row[2]
        # Get the feedback value
        feedback = row[3]
        # Create a dictionary with the date, user, JSON fields, and feedback
        date = row[0].strftime('%Y-%m-%d %H:%M:%S')
        entry = {'date': date, 'user': user_id, 'file': log['file'], 'action': log['action'], 'status': log['status'],
                'description': log['description'], 'feedback': feedback}
        data.append(entry)

    # Return the data as a JSON response
    return JsonResponse({'data': data}, safe=False)
    
@login_required
def user_table(request):
    user_id = request.user.id
    # Only display user logs code below
    query = """SELECT date, log, user_id, feedback FROM myapp_log WHERE user_id = {} ORDER BY date DESC""".format(user_id)
    with connection.cursor() as cursor:
        cursor.execute(query)
        rows = cursor.fetchall()

    # Create a list of dictionaries from the query results
    data = []
    for row in rows:
        # Parse the JSON string into a dictionary
        log = json.loads(row[1])
        # Get the user object based on the user_id
        user_id = row[2]
        # Get the feedback value
        feedback = row[3]
        # Create a dictionary with the date, user, JSON fields, and feedback
        date = row[0].strftime('%Y-%m-%d %H:%M:%S')
        entry = {'date': date, 'user': user_id, 'file': log['file'], 'action': log['action'], 'status': log['status'],
                'description': log['description'], 'feedback': feedback}
        data.append(entry)

    # Return the data as a JSON response
    return JsonResponse({'data': data}, safe=False)


@login_required
def users(request):
    # Make a request to the admin_table view to get the data
    context = {}
    data_user = user_table(request)
    user_dict = json.loads(data_user.content)
    token_count = UserTokenCount.objects.get(user=request.user).token_count
    user_profile = request.user.profile
    user = request.user
    all_user_profiles = Profile.objects.all()  # Retrieve all Profile objects

    # Pass the data as a context variable to the template
    # !!! ADMIN DATA ONLY DISPLAYED AND GET IF USER IS ADMIN !!!
    if request.user.profile.user_type == 1 or request.user.is_superuser or request.user.profile.user_type == 2:
        data_admin = admin_table(request)
        admin_dict = json.loads(data_admin.content)
        context['admin_data'] = admin_dict['data']

    context['user_data'] = user_dict['data']
    context['token_count'] = token_count
    context['user_profile'] = user_profile
    context['user'] = user
    context['all_user_profiles'] = all_user_profiles  # Add all_user_profiles to the context

    return render(request, 'user_page.html', context)

@login_required
@admin_required
def change_user_type(request, user_id):
    if request.method == 'POST':
        user_type = request.POST.get('user_type')
        user_profile = get_object_or_404(Profile, user__id=user_id)
        user_profile.user_type = user_type
        user_profile.save()

        user = user_profile.user
        if user_type == '1':
            user.is_superuser = True
            user.is_staff = True
            user.save()
        else:
            user.is_superuser = False
            user.is_staff = False
            user.save()
        
        user_type_display = user_profile.get_user_type_display()
        log_data = get_log_data(request.user, Action.CHANGE_USER_TYPE, user_type=user_type_display, description=f"{request.user.username} changed {user_profile.user.username}'s user type to {user_type_display}")
        create_log(request.user, log_data)
        messages.success(request, f'{user_profile.user.username}\'s user type has been changed to {user_type_display}.')
        return redirect('users')