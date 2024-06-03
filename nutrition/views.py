from django.shortcuts import render, redirect, get_object_or_404
from .models import  Club, CustomUser, Person
from .backends import CustomUserBackend
from random import shuffle, sample
from django.contrib.auth import login as auth_login, authenticate
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required

from django.core.files.storage import FileSystemStorage

from sports_nutrition.info import encrypt_data, decrypt_data

from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.http import Http404
from django.db import DatabaseError
from django.contrib.auth import update_session_auth_hash




def login_signup_view(request):
    if request.method == 'POST':
        form_type = request.POST.get('form_type')

        if form_type == 'login-form':
            email = request.POST['email']
            password = request.POST['password']
            backend = CustomUserBackend()

            user = backend.authenticate(
                request, email=email, password=password)

            if user:
                auth_login(request, user)
                messages.success(request, 'Welcome back!')
                return redirect('clubs')
            else:
                messages.error(request, 'Wrong password or email')
                return render(request, 'authentification/login.html', {'login_error': True})

        elif form_type == 'signup-form':
            name = request.POST['name']
            email = request.POST['email']
            password = request.POST['password']
            date_of_birth = request.POST['date_of_birth']
            sex = request.POST['sex']

            if CustomUser.objects.filter(email=email).exists():
                return render(request, 'authentification/login.html', {'signup_error': True, 'error_message': 'User with this email already exists.'})

           

            # Create User instance
            user = CustomUser.objects.create_user( email=email, password=password)
            
            # Create Person instance
            person = Person.objects.create(
                user=user, name=name, date_of_birth=date_of_birth, sex=sex)

            # Link Person to User if necessary
            # Assuming a one-to-one relationship between Person and CustomUser:
            # user.person = person
            # user.save()

        
            auth_login(request, user, backend='nutrition.backends.CustomUserBackend')

            messages.success(
                request, 'Welcome! Your account has been created successfully.')
            return redirect(reverse('home'))
        else:
            messages.error(
                request, 'Invalid form submission. Please check the form fields.')
            return render(request, 'authentification/login.html', {'signup_error': True, 'error_message': 'Invalid form submission. Please check the form fields.'})

    return render(request, 'authentification/login.html')


def home(request):
    user_scores = None
    name = None
    if request.user.is_authenticated:
        user = CustomUser.objects.get(email=request.user)
       
        # Fetch the user ID (adjust this based on your actual user identification logic)
        user_id = user.id
        

    return render(request, 'home.html')


def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
        messages.success(request, 'You have been logged out successfully.')
    else:
        messages.warning(request, 'You are not logged in.')
    # Optional: add a logout message
    messages.success(request, 'You have been logged out.')
    return redirect('home')


def reset_password_view(request):
    return render(request, 'authentification/reset_password.html')


@login_required
def clubs_views(request):
    current_user = request.user
    try:
        person = Person.objects.get(user=current_user)
        person_name = person.name
    except Person.DoesNotExist:
        person_name = "Unknown"

    club_types = [choice[0] for choice in Club.CLUB_TYPE_CHOICES]

    # Fetch all clubs from the database
    clubs = Club.objects.all()

    # Prepare the data for rendering
    club_data = []
    for club in clubs:
        # Prepare the logo URL
        logo_url = "/media/" + str(club.logo)
        club_data.append({
            'id': club.id,
            'logo': logo_url,
            'club_name': club.club_name,
            'club_type': club.club_type,
            'date_of_creation': club.created_at.strftime("%d-%m-%Y"),
        })

    if request.method == 'POST':
        form_name = request.POST.get('form_name')

        if form_name == 'updateclub':
            club_id = request.POST.get('club_id')
            club = get_object_or_404(Club, id=club_id)

            club_name = request.POST.get('club_name')
            club_type = request.POST.get('club_type')
            club_date_of_creation = request.POST.get('club_date_of_creation')

            # Check if the club name and type combination already exists, excluding the current club
            if Club.objects.filter(club_name=club_name, club_type=club_type).exclude(id=club.id).exists():
                messages.error(
                    request, "A club with the same name and type already exists!")
                return redirect('clubs_add')

            # Update club details
            club.club_name = club_name
            club.club_type = club_type
            club.created_at = club_date_of_creation

            # Check if a new logo file is uploaded
            if 'club_logo' in request.FILES:
                if club.logo:
                    # Delete old logo file from storage
                    club.logo.delete(save=False)
                club_logo = request.FILES['club_logo']
                fs = FileSystemStorage()
                filename = fs.save(club_logo.name, club_logo)
                club.logo = filename

            # Save the updated club details with error handling
            try:
                club.save()
                messages.success(request, "Club updated successfully!")
            except DatabaseError as e:
                messages.error(request, f"Database error occurred: {e}")
                return redirect('clubs_add')

            return redirect('clubs')

        elif form_name == 'deletclub':
            club_id = request.POST.get('club_id')
            print(club_id)
           

            club = Club.objects.get(id=club_id)

            # Delete the club with error handling
            try:
                club.delete()
                messages.success(request, "Club deleted successfully!")
            except DatabaseError as e:
                messages.error(request, f"Database error occurred: {e}")
                return redirect('clubs')

            return redirect('clubs')

    # Render the club management page
    return render(request, 'nutrition/manage_clubs/manage_clubs.html', {
        'person_name': person_name,
        'club_types': club_types,
        'club_data': club_data
    })
    
@login_required
def add_clubs_views(request):
    current_user = request.user
    try:
        person = Person.objects.get(user=current_user)
        person_name = person.name
    except Person.DoesNotExist:
        person_name = "Unknown"

    club_types = [choice[0] for choice in Club.CLUB_TYPE_CHOICES]

    if request.method == 'POST' and 'club_logo' in request.FILES:
        club_logo = request.FILES['club_logo']
        club_name = request.POST.get('club_name')
        club_type = request.POST.get('club_type')
        club_date_of_creation = request.POST.get('club_date_of_creation')

        # Check if the club already exists with the same name and type
        if Club.objects.filter(club_name=club_name, club_type=club_type).exists():
            messages.error(
                request, "A club with the same name and type already exists!")
            return redirect('clubs_add')

        # Encrypt the data before saving it to the database
        encrypted_club_name = encrypt_data(club_name)
        encrypted_club_type = encrypt_data(club_type)
        encrypted_club_date_of_creation = encrypt_data(club_date_of_creation)

        # Save the logo file
        fs = FileSystemStorage()
        filename = fs.save(club_logo.name, club_logo)
        uploaded_file_url = fs.url(filename)
        encrypted_url = encrypt_data(uploaded_file_url)
        print("file name ", filename)
        print("file url ", decrypt_data(encrypted_url))

        # Create the new club
        new_club = Club(
            club_name=club_name,
            club_type=club_type,
            logo=filename,
            created_at=club_date_of_creation
        )
        new_club.save()

        messages.success(request, "Club added successfully!")
        return redirect('clubs')

    return render(request, 'nutrition/manage_clubs/add_club.html', {'person_name': person_name, 'club_types': club_types})


def request_club_info_views(request, id):
    if request.method == 'GET' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        try:
            club = Club.objects.get(pk=id)
            club_data = {
                'id': club.id,
                'club_name': club.club_name,
                'club_type': club.club_type,
                'date_of_creation': club.created_at.strftime('%Y-%m-%d'),
                
               'logo_url': '/media/' + str(club.logo) if club.logo else ''
               # Add more fields if needed
            }
            print(club_data)
            return JsonResponse(club_data)
        except Club.DoesNotExist:
            return JsonResponse({'error': 'Club not found'}, status=404)
    return JsonResponse({'error': 'Invalid request'}, status=400)


@login_required
def account_views(request):
    current_user = request.user
    Unknown = "Unknown"
    try:
        person_email =request.user.email
        person_last_login = request.user.last_login
        person_date_creation = request.user.date_joined
        person = Person.objects.get(user=request.user)
        person_name = person.name
        person_sex = "Male" if person.sex == "M" else "Female" if person.sex == "F" else "Other"

        
        person_date_of_birth= person.date_of_birth
        context = { 'person_email':person_email, 'person_name':person_name, 'person_last_login': person_last_login,
                   'person_date_creation':person_date_creation, 'person_date_of_birth': person_date_of_birth, 'person_sex': person_sex,}
        print(context)
    except Person.DoesNotExist:
         context = { 'person_email':Unknown, 'person_name':Unknown, 'person_last_login': Unknown,
                   'person_date_creation':Unknown, 'person_date_of_birth': Unknown, 'person_sex': Unknown,}
         
         
    if request.method == 'POST':
            form_name = request.POST.get('form_name')
            if form_name == 'update_email':
                email = request.POST.get('email')
                password = request.POST.get('password')
                if not current_user.check_password(password):
                    messages.error(request, 'Incorrect password. Please try again.')
                    return redirect('account')
                request.user.email = email
                request.user.save()
                update_session_auth_hash(request, request.user)
                messages.success(request, 'Your email has been changed successfully.')

                return redirect('account')
            elif form_name == 'update_password':
                current_password = request.POST.get('currentPassword')
                new_password = request.POST.get('newPassword')
                new_password_confirm = request.POST.get('newPasswordConfirm')

                if not request.user.check_password(current_password):
                    messages.error(request, 'The current password you entered is incorrect.')
                    return redirect('account')

                if new_password != new_password_confirm:
                    messages.error(request, 'The new passwords you entered do not match.')
                    return redirect('account')

                request.user.set_password(new_password)
            
                request.user.save()
                update_session_auth_hash(request, request.user)
                messages.success(request, 'Your password has been changed successfully.')
                return redirect('account')
            elif form_name == 'delet_account':
                request.user.is_active = False
                request.user.save()
                logout(request)
                messages.success(request, 'Your Account has been deleted successfully.')

                return redirect('/')
            elif form_name == 'update_personal_details':

                id = request.user.id
                person = Person.objects.get(user=current_user)


                # Update the fields of the Personne object with the new values from the POST request
                person.name = request.POST.get('full_name')
                day_birth = request.POST.get('day')
                month_birth = request.POST.get('month')
                year_birth = request.POST.get('year')
                person.date_of_birth = f"{year_birth}-{month_birth}-{day_birth}"
                person.sex = request.POST.get('sex')

                # Save the updated Personne object
                person.save()
                messages.success(request, 'Your profile has been updated successfully!')
                return redirect('account')
          
    return render(request, 'profile/account.html', context)

def players_views(request):
    return render(request, 'nutrition/manage_players/manage_players.html')

def foods_views(request):
    return render(request, 'nutrition/manage_foods/manage_foods.html')


def archive_players_views(request):
    return render(request, 'profile/account.html')

def dashboard_views(request):
    return render(request, 'nutrition/dashboard.html')