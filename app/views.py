from django.utils.http import urlsafe_base64_decode
from django.urls import reverse_lazy
from django.views import generic
from .models import CustomUser,Qada,Municipal
from django.shortcuts import redirect,render
from django.contrib.auth.views import LoginView
from django.http import HttpResponse
from django.utils.translation import gettext_lazy as _
from .forms import PasswordResetForm,CustomUserCreationForm,CaptchaForm
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth.forms import PasswordResetForm
from django.http import JsonResponse

UserModel = get_user_model()


class SignUpView(generic.CreateView):
    form_class = CustomUserCreationForm
    template_name = "registration/signup.html"
    def get_success_url(self):
        return reverse_lazy('signup_success')
    def form_valid(self, form):
        response = super().form_valid(form)

        user = CustomUser.objects.get(username=form.cleaned_data['username'])
        user.calculate_age()

        return response
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['qada_options'] = Qada.objects.none()
        return context

    def post(self, request):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)

        error_messages = form.errors.as_text()
        error_message = f"<h4>خطأ في الإدخال:</h4>{error_messages}"
        return HttpResponse(error_message, status=400)

class CustomLoginView(LoginView):
    template_name = 'registration/login.html'
    redirect_authenticated_user = True
    def post(self, request):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)

        error_messages = form.errors.as_text()
        error_message = f"<h4>خطأ في الإدخال:</h4>{error_messages}"
        return HttpResponse(error_message, status=400)



def forget_password(request):
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            form.save(request=request)
            # Redirect to a success page or display a success message
            return render(request, 'password_reset/reset_done.html')
    else:
        form = PasswordResetForm()
    return render(request, 'password_reset/forget_password.html', {'form': form})

def reset_password_confirm(request, uidb64, token):
     User = get_user_model()
     try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
     except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
     if user is not None and default_token_generator.check_token(user, token):
        if request.method == 'POST':
            form = SetPasswordForm(user, request.POST)
            if form.is_valid():
                form.save()
                # Password has been successfully reset
                return render(request, 'password_reset/reset_complete.html')
        else:
            form = SetPasswordForm(user)
        return render(request, 'password_reset/reset_form.html', {'form': form})
     else:

      return render(request, 'password_reset/reset_invalid.html')

def reset_password_done(request):
     return render(request, 'password_reset/reset_done.html')

def reset_password_complete(request):
    return render(request, 'password_reset/reset_complete.html')

def get_qada_options(request):
    province_id = request.GET.get('province_id')

    if province_id:
        qada_options = Qada.objects.filter(province_id=province_id).values('id', 'name')
    else:
        qada_options = []

    return JsonResponse(list(qada_options), safe=False)

def get_municipal_options(request):
    qada_id = request.GET.get('qada_id')

    if qada_id:
        municipal_options = Municipal.objects.filter(qada_id=qada_id).values('id', 'name')

    return JsonResponse(list(municipal_options), safe=False)
                                                                        

def afterlogin(request):
    form = CaptchaForm(request.POST)
    if request.user.is_superuser :
        users = CustomUser.objects.all() 
        if request.method == 'POST':   
            user_id = request.POST.get('user_id') 
            user = CustomUser.objects.get(pk=user_id) 
            user.delete() 
            return redirect('afterlogin')  
        return render(request, 'admin.html',{'users': users})
    
    else:
     if request.method == 'POST':
         if form.is_valid():
            return render(request, 'menu.html')
         else:
            form = CaptchaForm()

    return render(request, 'registration/captcha.html', {'form': form})
    
