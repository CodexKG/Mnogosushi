from django.urls import path 
from apps.users.views import register, user_login, profile
from django.contrib.auth import views as auth_views #import this


urlpatterns = [
    path('register/', register, name = "register"),
    path('login/', user_login, name = "login"),
    path('profile/<str:username>', profile, name = "profile"),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="users/password_reset_confirm.html"), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='users/password_reset_complete.html'), name='password_reset_complete'),      
]   