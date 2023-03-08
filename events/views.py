from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, redirect, reverse

from django.views import View
from .models import Event

def index(request):
    return render(request, 'index.html', {})

class RegisterView(View):
    def get(self, request):
        return render(request, 'registration/register.html', { 'form': UserCreationForm() })

    def post(self, request):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            return redirect(reverse('login'))

        return render(request, 'registration/register.html', { 'form': form })

class LoginView(View):
    def get(self, request):
        return render(request, 'registration/login.html', { 'form': AuthenticationForm() })

    def post(self, request):
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = authenticate(
                request,
                username=form.cleaned_data.get('username'),
                password=form.cleaned_data.get('password')
            )

            if user is None:
                return render(
                    request,
                    'registration/login.html',
                    { 'form': form, 'invalid_creds': True}
                )

            try:
                form.confirm_login_allowed(user)
            except ValidationError:
                return render(
                    request,
                    'registration/login.html',
                    { 'form': form, 'invalid_creds': True}
                )

            login(request, user)

            return redirect(reverse('events'))

class EventsView(LoginRequiredMixin, View):
    def get(self, request):
        events = Event.objects.filter(owner=request.user).all()

        context = {
            'events': events
        }

        return render(request, 'events.html', context)