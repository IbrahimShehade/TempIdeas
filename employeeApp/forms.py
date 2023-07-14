from django import forms
from .models import Employee,Province,Qada,Municipal
from captcha.fields import ReCaptchaField

class EmployeeLoginForm(forms.ModelForm):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
    province = forms.ModelChoiceField(queryset=Province.objects.all())
    qada = forms.ModelChoiceField(queryset=Qada.objects.all())
    municipal = forms.ModelChoiceField(queryset=Municipal.objects.all())


    class Meta:
        model = Employee
        fields = ('username', 'password', 'province', 'qada', 'municipal')
   

    def __str__(self):
        return self.username


class CaptchaForm(forms.Form):
    captcha = ReCaptchaField()
