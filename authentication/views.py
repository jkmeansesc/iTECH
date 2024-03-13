from django.contrib.auth.models import User
from django.shortcuts import render
from django.shortcuts import redirect
from django.urls import reverse
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from .forms import UserForm, UserProfileForm
from .models import UserProfile
from blog.utils import send_mails


def register(request):
    error_message = ""
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            # Check the password length
            if len(user_form.cleaned_data['password']) < 6:
                error_message += "Password length must be greater than 6."
                return render(request, 'authentication/register.html',
                          {'user_form': user_form, 'profile_form': profile_form, 'error_message': error_message})
            
            user = user_form.save()
            user.set_password(user.password)  # Hash the password
            user.save()

            profile = profile_form.save(commit=False)  # Don't save to database yet
            profile.user = user
            profile.save()
            return redirect(reverse('authentication:login'))
        else:
            # Check the errors
            if user_form.errors:
                error_message += "The user has been registered, please try another one."

            # Invalid form or forms, come back to the registration page, send the error message
            return render(request, 'authentication/register.html',
                          {'user_form': user_form, 'profile_form': profile_form, 'error_message': error_message})
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()
        return render(request, 'authentication/register.html',
                    {'user_form': user_form, 'profile_form': profile_form, 'error_message': error_message})


def user_login(request):
    error_message = ""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Check the username and password
        user = authenticate(username=username, password=password)
        
        if user:
            login(request, user)
            return redirect(reverse('blog:index'))
        else:
            error_message = "Invalid login details supplied or your account is disabled."
            print(error_message)
            return render(request, 'authentication/login.html', {'error_message': error_message})
    else:
        return render(request, 'authentication/login.html', {'error_message': error_message})

@login_required
def user_logout(request):
    logout(request)
    return redirect(reverse('blog:index'))


def set_username(request):
    # get the username from the post request
    username = request.POST.get('username')
    # get the current user
    user = request.user
    # set the username of the current user to the username from the post request
    user.username = username
    # save the current user
    user.save()
    # redirect to the profile settings page
    return redirect(reverse('blog:profile_settings'))


def set_email(request):
    # get the email from the post request
    email = request.POST.get('email')
    # get the current user
    user = request.user
    # set the email of the current user to the email from the post request
    user.email = email
    # save the current user
    user.save()
    return redirect(reverse('blog:profile_settings'))


def set_avatar(request):
    # check if the image is None
    if request.FILES.get("image") is None:
        return redirect(reverse('blog:profile_settings'))
    
    avatar = request.FILES['image']
    userProfile = request.user.userProfile
    userProfile.picture = avatar
    userProfile.save()

    return redirect(reverse('blog:profile_settings'))


def set_password(request):
    # get the password and password1 from the post request
    password = request.POST.get('password')
    password1 = request.POST.get('password1')
    if password != password1:
        print("The two passwords are not the same")
        return render(request, 'blog/profile_settings.html', {'error_message': 'The two passwords are not the same'})
        # return redirect(reverse('blog:profile_settings'), {'error_message': 'The two passwords are not the same'})
    else:
        if len(password) >= 6:
            # get the current user
            user = request.user
            # set the password of the current user to the password from the post request
            user.set_password(password)
            # save the current user
            user.save()
            return redirect(reverse('authentication:login'))

        else:
            return render(request, 'blog/profile_settings.html', {'error_message': 'Password length must be greater than 6.'})


def block_user(request, user_id):
    # get the user with the user_id
    user = User.objects.get(id=user_id)
    user.is_active = False
    user.save()
    return redirect(reverse('blog:manage_all_accounts'))


def password_reset(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        user = User.objects.filter(email=email).first()
        if user is not None:
            userProfile = user.userProfile
            userProfile.generate_token()
            subject = "Reset your password"

            message = "Please click the link below to reset your password: https://zhengkangwu.pythonanywhere.com/authentication/password_reset_confirm/" + userProfile.token
            from_email = "2079459973@qq.com"
            recipient_list = [email, ]
            send_mails(subject, message, from_email, recipient_list)

            return render(request, 'authentication/password_reset.html', {'success_message': 'We have sent you an email with a link to reset your password.'})
        else:
            return render(request, 'authentication/password_reset.html', {'error_message': 'No user found with that email address.'})

    else:
        return render(request, 'authentication/password_reset.html')

def password_reset_confirm(request, token):
    if request.method == 'POST':
        new_password1 = request.POST.get('new_password1')
        new_password2 = request.POST.get('new_password2')
        if new_password1 != new_password2:
            return render(request, 'authentication/password_reset_confirm.html', {'token': token,'error_message': 'The two passwords are not the same'})
        else:
            if len(new_password1) >= 6:
                userProfile = UserProfile.objects.filter(token=token).first()
                if userProfile is not None and userProfile.is_token_valid():
                    user = userProfile.user
                    user.set_password(new_password1)
                    user.save()
                    # set the token to None
                    userProfile.token = None
                    userProfile.save()
                    
    
                    return redirect(reverse('authentication:login'))
                else:
                    return render(request, 'authentication/password_reset_confirm.html', {'token': token, 'error_message': 'The token is invalid or expired.'})
            else:
                return render(request, 'authentication/password_reset_confirm.html', {'token': token, 'error_message': 'Password length must be greater than 6.'})
    else:
        return render(request, 'authentication/password_reset_confirm.html', {'token': token})



