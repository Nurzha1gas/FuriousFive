from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.http import require_GET
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib import messages

from .forms import SignUpForm, UserProfileForm, PasswordChangeForm


def user_login(request):
    if request.user.is_authenticated:
        return redirect('core:home')

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('core:home')  # Redirect to home page after successful login
        else:
            # Invalid login
            error = 'Invalid username or password.'
            messages.error(request, error)
            return render(request, 'login.html', {'error': 'Invalid username or password.'})
    else:
        return render(request, 'login.html')


@login_required
def home_view(request):
    return render(request, 'home.html', {'username': request.user.username})

@login_required
def logout_view(request):
    logout(request)
    return render(request, 'login.html')


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your account has been created successfully. You can now log in.')
            return redirect('core:login')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})


@login_required
def profile(request):
    user = request.user
    if request.method == 'POST':
        if 'update_profile' in request.POST:
            print('update profile')
            profile_form = UserProfileForm(request.POST)
            password_form = PasswordChangeForm() 
            if profile_form.is_valid():
                print("valid form")
                # Update user profile
                first_name = profile_form.cleaned_data['first_name']
                last_name = profile_form.cleaned_data['last_name']
                email = profile_form.cleaned_data['email']

                user.first_name = first_name
                user.last_name = last_name
                user.email = email
                user.save()
                messages.success(request, 'Your profile has been updated successfully.')
                return redirect('core:profile')
            else:
                for field, errors in profile_form.errors.items():
                    for error in errors:
                        messages.error(request, f'Error in {field}: {error}')
                # messages.error(request, 'Please correct the errors below.')
        elif 'change_password' in request.POST:
            print('change pas')
            password_form = PasswordChangeForm(request.POST)
            profile_form = UserProfileForm(instance=user)
            if password_form.is_valid():
                current_password = password_form.cleaned_data['current_password']
                new_password = password_form.cleaned_data['new_password']
                repeat_new_password = password_form.cleaned_data['repeat_new_password']
                if user.check_password(current_password) and new_password == repeat_new_password:
                    user.set_password(new_password)
                    user.save()
                    # Update session authentication hash to prevent automatic logout
                    update_session_auth_hash(request, user)
                    messages.success(request, 'Your password has been changed successfully.')
                    return redirect('core:profile')
                else:
                    # Invalid password or new password doesn't match
                    messages.error(request, 'Invalid password or new password mismatch')
                    password_form.add_error('current_password', 'Invalid password or new password mismatch')
            else:
                for field, errors in password_form.errors.items():
                    for error in errors:
                        messages.error(request, f'Error in {field}: {error}')
    else:
        print('nothing')
        profile_form = UserProfileForm(instance=user)
        password_form = PasswordChangeForm()

    return render(request, 'profile.html', {'form': profile_form, 'user': user, 'password_form': password_form})


@login_required
def delete_account(request):
    if request.method == 'POST':
        user = request.user
        # Perform any additional cleanup tasks before deleting the account
        user.delete()
        logout(request)
        messages.success(request, 'Your account has been deleted successfully.')
        return redirect('core:home')  # Redirect to home page or any other page after deletion
    else:
        return HttpResponseNotAllowed(['POST'])


@login_required
def history_view(request):
    return render(request, 'history.html')


@login_required
def notifications_view(request):
    return render(request, 'notifications.html')