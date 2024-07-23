from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.views.generic import TemplateView
from django.shortcuts import redirect, render, get_object_or_404

from myapp.forms import SignUpForm


# Create your views here.


class HomeView(TemplateView):
    template_name = 'home.html'


class CustomLoginView(LoginView):
    template_name = 'login.html'

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
