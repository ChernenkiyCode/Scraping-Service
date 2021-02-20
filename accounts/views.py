import datetime

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, get_user_model
from .forms import UserLoginForm, UserRegistrationForm, UserUpdateForm, ContactForm
from django.contrib import messages
from scraping.models import Error

User = get_user_model()


def login_view(request):
    form = UserLoginForm(request.POST or None)
    if form.is_valid():
        email = form.cleaned_data.get('email')
        password = form.cleaned_data.get('password')
        user = authenticate(request, email=email, password=password)
        login(request, user)
        messages.success(request, 'Вход c аккаунта %s завершен' % email)
        return redirect('home')
    return render(request, 'accounts/login.html', {'form': form})


def logout_view(request):
    email = request.user.email
    logout(request)
    messages.error(request, 'Выход с аккаунта %s завершен' % email)
    return redirect('home')


def register_view(request):
    form = UserRegistrationForm(request.POST or None)
    if form.is_valid():
        new_user = form.save(commit=False)
        new_user.set_password(form.cleaned_data['password'])
        new_user.save()
        messages.success(request, 'Пользователь добавлен %s в систему' % new_user.email)
        return render(request, 'accounts/register_done.html', {'new_user': new_user})
    return render(request, 'accounts/register.html', {'form': form})


def user_update_view(request):
    if request.user.is_authenticated:
        user = request.user
        if request.method == 'POST':
            form = UserUpdateForm(request.POST)
            if form.is_valid():
                user.city = form.cleaned_data['city']
                user.language = form.cleaned_data['language']
                user.send_email = form.cleaned_data['send_emails']
                user.save()
                messages.success(request, 'Данные пользователя %s обновлены' % user.email)
                return redirect('home')
            else:
                return render(request, 'accounts/update.html', {'form': form})
        else:
            form = UserUpdateForm(initial={
                'city': user.city, 'language': user.language, 'send_emails': user.send_email})
        return render(request, 'accounts/update.html', {'form': form})
    else:
        return redirect('login')


def user_delete_view(request):
    if request.user.is_authenticated:
        usr = request.user
        if request.method == 'POST':
            user = User.objects.get(pk=usr.pk)
            user.delete()
            messages.warning(request, 'Пользователь %s удален' % usr.email)
            return redirect('home')
        else:
            return render(request, 'accounts/confirm_delete.html')
    return redirect('login')


def contact_view(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = ContactForm(request.POST)
            if form.is_valid():
                data = {
                    'user_email': request.user.email,
                    'city': form.cleaned_data['city'],
                    'language': form.cleaned_data['language'],
                    'message': form.cleaned_data['message']
                }
                qs = Error.objects.filter(timestamp=datetime.date.today())
                if qs.exists():
                    err = qs.first()
                    err.data['Users_requests'].append(data)
                    err.save()
                else:
                    Error.objects.create(data={'Users_requests': [data]})
                messages.success(request, 'Ваш запрос отправлен администрации')
                return redirect('home')
            else:
                return render(request, 'accounts/contact_form.html', {'form': form})
        else:
            form = ContactForm()
            return render(request, 'accounts/contact_form.html', {'form': form})
    return redirect('login')
