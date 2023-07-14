
from django.urls import path
from .views import login_employee,success_page,get_qada_options,get_municipal_options,captchaView
urlpatterns = [
     path('', login_employee, name='login-employee'),
     path('success/', success_page, name='success-page'),
     path('get_qada_options/', get_qada_options, name='get_qada_options'),
     path('get_municipal_options/', get_municipal_options, name='get_municipal_options'),

      path('captcha/', captchaView, name='captcha'),
]
