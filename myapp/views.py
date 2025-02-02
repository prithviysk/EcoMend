from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView, PasswordChangeDoneView
from django.contrib.sessions.models import Session
from django.http import HttpResponse
from django.contrib.auth import login
from django.utils import timezone
from django.utils.timezone import now
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView, ListView, DetailView, FormView
from django.shortcuts import redirect, render, get_object_or_404
from myapp.models import Category, PlasticListing
from myapp.forms import SignUpForm, ProfileUpdateForm, ContactForm, CategoryPlasticListingForm, PlasticListingForm
from myapp.models import Profile, LoginHistory
from django.utils.decorators import method_decorator


class AboutView(TemplateView):
    template_name = 'about.html'


class HomeView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context


class CustomLoginView(LoginView):
    template_name = 'login.html'


class CustomLogoutView(LogoutView):
    template_name = 'logged_out.html'

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
            return redirect('view_profile')
    else:
        form = ProfileUpdateForm(instance=profile)
    return render(request, 'update_profile.html', {'form': form})


def superuser_required(view_func):
    decorated_view_func = user_passes_test(lambda u: u.is_superuser, login_url='home')(view_func)
    return decorated_view_func


@superuser_required
def site_statistics(request):
    if request.method == 'GET':
        return render(request, 'site_statistics.html')


def get_active_sessions():
    # Filter sessions that have not expired
    sessions = Session.objects.filter(expire_date__gte=now())
    return sessions


@user_passes_test(lambda u: u.is_superuser)
def site_statistics(request):
    visits = request.session.get('visits', 0)
    last_visit = request.session.get('last_visit', 'Never')

    # Get active sessions
    active_sessions = get_active_sessions()
    session_count = active_sessions.count()

    return render(request, 'site_statistics.html', {
        'visits': visits,
        'last_visit': last_visit,
        'active_sessions': session_count,
        'sessions': active_sessions,
    })


@csrf_exempt
def track_visit(request):
    session = request.session
    now = timezone.now()
    if 'visits' not in session:
        session['visits'] = 1
    else:
        session['visits'] += 1

    session['last_visit'] = now.strftime('%Y-%m-%d %H:%M:%S')
    session.save()

    return HttpResponse('Visit tracked')


def get_active_sessions():
    sessions = Session.objects.filter(expire_date__gte=now())
    return sessions


@method_decorator(login_required, name='dispatch')
class CustomPasswordChangeView(PasswordChangeView):
    template_name = 'password_change.html'
    success_url = '/password_change/done/'

@login_required
def login_history(request):
    login_history = LoginHistory.objects.filter(user=request.user).order_by('-timestamp')
    return render(request, 'login_history.html', {'login_history': login_history})


class CategoryListView(ListView):
    model = Category
    template_name = 'category_list.html'
    context_object_name = 'categories'


class CategoryDetailView(DetailView):
    model = Category
    template_name = 'category_detail.html'
    context_object_name = 'category'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['listings'] = PlasticListing.objects.filter(category=self.object)
        return context


@method_decorator(login_required, name='dispatch')
class CustomPasswordChangeDoneView(PasswordChangeDoneView):
    template_name = 'password_change_done.html'

@login_required
def new_category_plastic_listing(request, pk):
    category = get_object_or_404(Category, pk=pk)

    if request.method == 'POST':
        form = CategoryPlasticListingForm(request.POST, request.FILES, category=category)
        if form.is_valid():
            listing = form.save(commit=False)
            listing.category = category
            listing.seller = request.user
            listing.save()
            return redirect('category_detail', pk=pk)
    else:
        form = CategoryPlasticListingForm(category=category)

    context = {
        'form': form,
        'category': category,
    }
    return render(request, 'new_category_plastic_listing.html', context)

class CategoryDetailViewABS(DetailView):
    model = Category
    template_name = 'category_detail_abs.html'
    context_object_name = 'category'

class ContactFormView(FormView):
    template_name = 'contact_form.html'
    form_class = ContactForm
    success_url = '/thank-you/'

    def form_valid(self, form):
        return super().form_valid(form)


class MarketPlaceView(ListView):
    model = PlasticListing
    template_name = 'marketplace.html'
    context_object_name = 'listings'

    def get_queryset(self):
        queryset = PlasticListing.objects.all()

        # Filtering
        seller = self.request.GET.get('seller')
        min_price = self.request.GET.get('min_price')
        max_price = self.request.GET.get('max_price')
        category = self.request.GET.get('category')
        sort_by_date = self.request.GET.get('sort_by_date')

        if seller:
            queryset = queryset.filter(seller__username__icontains=seller)
        if min_price:
            queryset = queryset.filter(price__gte=min_price)
        if max_price:
            queryset = queryset.filter(price__lte=max_price)
        if category:
            queryset = queryset.filter(category__name__icontains=category)
        if sort_by_date:
            queryset = queryset.order_by('date_listed' if sort_by_date == 'asc' else '-date_listed')

        return queryset

@login_required
def new_plastic_listing(request):
    if request.method == 'POST':
        form = PlasticListingForm(request.POST, request.FILES)
        if form.is_valid():
            listing = form.save(commit=False)
            listing.seller = request.user
            listing.save()
            return redirect('listing_detail', pk=listing.pk)
    else:
        form = PlasticListingForm()
    return render(request, 'new_plastic_listing.html', {'form': form})


class MyListingsView(LoginRequiredMixin, ListView):
    model = PlasticListing
    template_name = 'my_listings.html'
    context_object_name = 'listings'

    def get_queryset(self):
        return PlasticListing.objects.filter(seller=self.request.user)


class ListingDetailView(DetailView):
    model = PlasticListing
    template_name = 'listing_detail.html'
    context_object_name = 'listing'