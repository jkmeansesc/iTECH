from django.contrib.auth.models import User
from django.shortcuts import render
from django.shortcuts import redirect
from django.urls import reverse
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from .forms import UserForm, UserProfileForm
from .models import UserProfile


def register(request):
    registered = False
    error_message = ""

    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():

            user = user_form.save()
            user.set_password(user.password)  # Hash the password
            user.save()

            profile = profile_form.save(commit=False)  # Don't save to database yet
            profile.user = user

            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']

            profile.save()

            registered = True
        else:

            # Check the errors
            if user_form.errors:
                error_message += f"User form errors: {user_form.errors}"
            if profile_form.errors:
                error_message += f"Profile form errors: {profile_form.errors}"

            print(user_form.errors, profile_form.errors)

            # Invalid form or forms, come back to the registration page, send the error message
            return render(request, 'authentication/register.html',
                          {'user_form': user_form, 'profile_form': profile_form, 'registered': registered,
                           'error_message': error_message})
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    return render(request, 'authentication/register.html',
                  {'user_form': user_form, 'profile_form': profile_form, 'registered': registered,
                   'error_message': error_message})


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user:
            # is the account active? It could have been disabled.
            if user.is_active:
                login(request, user)
                return redirect(reverse('blog:index'))
            else:
                return HttpResponse("Your Rango account is disabled.")
        else:
            print(f"Invalid login details: {username}, {password}")
            return HttpResponse("Invalid login details supplied.")
    else:
        return render(request, 'authentication/login.html')


@login_required
def user_logout(request):
    logout(request)
    return redirect(reverse('blog:index'))


def password_reset(request):
    return render(request, 'authentication/password_reset.html')


def set_username(request):
    # 得到post请求中的username
    username = request.POST.get('username')
    # 得到当前用户
    user = request.user
    # 将当前用户的username设置为post请求中的username
    user.username = username
    # 保存当前用户
    user.save()
    # 返回到设置用户名页面
    return redirect(reverse('blog:profile_settings'))


def set_email(request):
    # 得到post请求中的email
    email = request.POST.get('email')
    # 得到当前用户
    user = request.user
    # 将当前用户的email设置为post请求中的email
    user.email = email
    # 保存当前用户
    user.save()
    return redirect(reverse('blog:profile_settings'))


def set_avatar(request):
    avatar = request.FILES['image']
    userProfile = request.user.userProfile
    userProfile.picture = avatar
    userProfile.save()

    return redirect(reverse('blog:profile_settings'))


def set_password(request):
    # 得到post请求中的password
    password = request.POST.get('password')
    # 得到当前用户
    user = request.user
    # 将当前用户的password设置为post请求中的password
    user.set_password(password)
    # 保存当前用户
    user.save()
    return redirect(reverse('authentication:login'))

