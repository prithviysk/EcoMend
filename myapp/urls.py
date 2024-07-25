from django.urls import path
from . import views
from .views import CustomLoginView, CustomLogoutView, view_profile, update_profile, login_history, site_statistics, \
    track_visit

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('signup/', views.signup, name='signup'),
    path('profile/', view_profile, name='view_profile'),
    path('profile/update/', update_profile, name='update_profile'),
    path('profile/login_history/', login_history, name='login_history'),
    path('site-statistics/', site_statistics, name='site_statistics'),
    path('track-visit/', track_visit, name='track_visit'),
    path('categories/', views.CategoryListView.as_view(), name='category_list'),
    path('categories/<int:pk>/', views.CategoryDetailView.as_view(), name='category_detail'),
    path('categories/<int:pk>/new/', views.new_category_plastic_listing, name='new_plastic_listing'),
    path('about/', views.AboutView.as_view(), name='about'),
    path('contact/', views.ContactFormView.as_view(), name='contact_form'),
]
