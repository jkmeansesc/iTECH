from django.shortcuts import render
from django.shortcuts import redirect
from django.urls import reverse
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


from .forms import UserForm, UserProfileForm
from .models import UserProfile
from django.core.mail import send_mail
import secrets
from django.utils import timezone




def register(request):
    registered = False

    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password) # Hash the password
            user.save()

            profile = profile_form.save(commit=False) # Don't save to database yet
            profile.user = user


            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']

            profile.save()

            registered = True
        else:
            print(user_form.errors, profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    return render(request, 'authentication/register.html', {'user_form': user_form, 'profile_form': profile_form, 'registered': registered})

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
    if request.method == 'POST':
        email = request.POST.get('email')
        # 找到用户
        user = UserProfile.objects.get(user__email=email)
        if user:
            # 生成token和过期时间
            reset_token = secrets.token_urlsafe(32)
            # 设置三十分钟后过期
            expiry_time = timezone.now() + timezone.timedelta(minutes=30)
            # 更新数据库
            user.reset_token = reset_token
            user.reset_token_expiry = expiry_time
            user.save()
            # 发送邮件
            subject = "Reset password"
            message = "please click the link to reset your password: http://127.0.0.1:8000/authentication/password_reset_confirm/?token=" + reset_token
            from_email = "2079459973@qq.com"
            recipient_list = [email, ]
            send_mail(subject=subject, from_email=from_email, recipient_list=recipient_list, message=message)
            return render(request, 'authentication/password_reset.html', context={"success": True, "error": False})
        else:
            return render(request, 'authentication/password_reset.html', context={"success": False, "error": True})
    else:
        
        return render(request, 'authentication/password_reset.html', context={"success": False, "error": False})



def password_reset_confirm(request):
    if request.method == 'POST':
        token = request.POST.get('token')
        user = UserProfile.objects.get(reset_token=token)
        
        if user:
            if user.reset_token_expiry > timezone.now():
                new_password = request.POST.get('new_password1')
                user.user.set_password(new_password)
                user.user.save()

                return redirect(reverse('authentication:login'))
        return HttpResponse("The token has expired")

    else:

        token = request.GET.get('token')
        user = UserProfile.objects.get(reset_token=token)
        if user:
            # 如果没有过期
            if user.reset_token_expiry > timezone.now():
                return render(request, 'authentication/password_reset_confirm.html', context={"token": token})
            else: 
                return HttpResponse("The token has expired")
        else:
            return HttpResponse("Invalid token")