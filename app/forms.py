from django import forms
from .models import CustomUser,Province,Qada,Municipal
from django.core.exceptions import ValidationError
from datetime import date
from phonenumber_field.widgets import PhoneNumberPrefixWidget
from django.contrib.auth.forms import PasswordResetForm as DjangoPasswordResetForm
from phonenumber_field.formfields import PhoneNumberField
from captcha.fields import ReCaptchaField

old_date = date(1920,1,1)
def validate_entry_date(value):
    if value >= date.today():
        raise ValidationError('Entry date must be before today.')
    elif value <= old_date:
        raise ValidationError('Enter valid date.')


class CustomUserCreationForm(forms.ModelForm):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(label="Confirm Password", widget=forms.PasswordInput)
    date_of_birth = forms.DateField(widget=forms.DateInput
    (attrs={'type': 'date'}, format='%d/%m/%yyyy'), label='Date of Birth', validators=[validate_entry_date])
    
    province = forms.ModelChoiceField(queryset=Province.objects.all())
    qada = forms.ModelChoiceField(queryset=Qada.objects.all())
    municipal = forms.ModelChoiceField(queryset=Municipal.objects.all())
    
    middle_name = forms.CharField(required=True,max_length=100)
    mobile_phone = PhoneNumberField(
        required=True,widget=PhoneNumberPrefixWidget(initial='LB')
        ) 
   
    class Meta:
        model = CustomUser
        fields = ['username', 'first_name', 'last_name', 'email', 'password', 'confirm_password', 'date_of_birth'
                  , 'province', 'qada','municipal', 'middle_name', 'mobile_phone']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['qada'].queryset = Qada.objects.none()
        self.fields['municipal'].queryset = Municipal.objects.none()

        if 'province' in self.data:
            try:
                province_id = int(self.data.get('province'))
                self.fields['qada'].queryset = Qada.objects.filter(province_id=province_id)
            except (ValueError, TypeError):
                pass

        if 'qada' in self.data:
            try:
                qada_id = int(self.data.get('qada'))
                self.fields['municipal'].queryset = Municipal.objects.filter(qada_id=qada_id)
            except (ValueError, TypeError):
                pass

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")

        return cleaned_data




class PasswordResetForm(DjangoPasswordResetForm):
    email = forms.EmailField(label='Email', max_length=254, widget=forms.EmailInput(attrs={'autocomplete': 'email'}))


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].widget.attrs.update({'class': 'form-control'})


    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not email:
            raise forms.ValidationError('Please enter your email address.')
        return email


    def save(self, request=None, **kwargs):
        """
        Generates a one-use only link for resetting password and sends to the user.
        """
        email = self.cleaned_data["email"]
        self.cleaned_data["email"] = email.lower() if email else None
        super().save(request, **kwargs)

class CaptchaForm(forms.Form):
    captcha = ReCaptchaField()

    