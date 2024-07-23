from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.views.generic import TemplateView
from django.shortcuts import redirect, render, get_object_or_404

from myapp.forms import SignUpForm, ProfileUpdateForm
from myapp.models import Profile, LoginHistory


# Create your views here.


class HomeView(TemplateView):
    template_name = 'home.html'


class CustomLoginView(LoginView):
    template_name = 'login.html'

class CustomLogoutView(LogoutView):
    template_name = 'logout.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_login_page'] = True
        return context


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

@login_required
def view_profile(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    return render(request, 'view_profile.html', {'profile': profile})

@login_required
def update_profile(request):
    profile = Profile.objects.get(user=request.user)
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile_view')
    else:
        form = ProfileUpdateForm(instance=profile)
    return render(request, 'update_profile.html', {'form': form})

@login_required
def login_history(request):
    login_history = LoginHistory.objects.filter(user=request.user).order_by('-timestamp')
    return render(request, 'login_history.html', {'login_history': login_history})
