from django.urls import path
from .views import get_municipal_options,get_qada_options,SignUpView,afterlogin,CustomLoginView,forget_password,reset_password_confirm,reset_password_done,reset_password_complete
from django.views.generic.base import TemplateView
from django.contrib.auth.views import LogoutView
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from .models import CustomUser

uidb64 = urlsafe_base64_encode(force_bytes(CustomUser.pk))


urlpatterns = [
    path("", SignUpView.as_view(), name="signup"),
    path('afterlogin/', afterlogin, name='afterlogin'),
    path('login',CustomLoginView.as_view(),name='login'),
    path('signup/success/',TemplateView.as_view(template_name='welcome.html'), name='signup_success'),
    path('success/',LogoutView.as_view(template_name='home.html'), name='logout'),
   
    path('password-reset/', forget_password, name='password_reset'),
    path('reset/<uidb64>/<token>/', reset_password_confirm, name='password_reset_confirm'),
    path('reset/done/',reset_password_done, name='password_reset_done'),
    path('password-reset-complete/', reset_password_complete, name='password_reset_complete'),

    path('get_qada_options/', get_qada_options, name='get_qada_options'),
    path('get_municipal_options/', get_municipal_options, name='get_municipal_options'),
    
   
  
]
            