from django.shortcuts import render

from app.views import get_qada_options
from .forms import EmployeeLoginForm,CaptchaForm
from django.shortcuts import redirect
from django.contrib.auth import login
from .models import Employee,Qada

def login_employee(request):
   
    if request.method == 'POST':
        form = EmployeeLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            municipal = form.cleaned_data.get('municipal')  

            employee = Employee.objects.filter(username=username).first()
            
            if employee is not None:
              
                if employee.password == password and employee.municipal == municipal:
                    login(request, employee)
                    return redirect('captcha')
                else:
                    form.add_error('password', 'تأكد من البيانات المدخلة')
            else:
                form.add_error('username', 'Employee does not exist')
    else:
        form = EmployeeLoginForm()
   

    return render(request, 'login.html', {'form': form})
    


def success_page(request):
    return render(request, 'success_page.html')
    
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


def captchaView(request):
    if request.method == 'POST':
        form = CaptchaForm(request.POST)
        if form.is_valid():
            return redirect('success-page')  
    else:
        form = CaptchaForm()

    return render(request, 'captcha.html', {'form': form})
