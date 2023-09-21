from django.urls import path
from .views import login_view, user_profile
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('login/', login_view, name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/login/'), name='logout'),
    path('', user_profile, name='user_profile'),
]