from django.urls import path
from . import views
from .views import CustomLoginView, CustomLogoutView, view_profile, update_profile, login_history

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('signup/', views.signup, name='signup'),
    path('profile/', view_profile, name='view_profile'),
    path('profile/update/', update_profile, name='update_profile'),
    path('profile/login_history/', login_history, name='login_history'),
]