from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import PasswordChangeForm
class LoginForm(forms.Form):
    username = forms.CharField(label='Имя аккаунта', max_length=100)
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)

class RegisterForm(forms.ModelForm):
    username = forms.CharField(label="Username")
    password = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Password Repeat", widget=forms.PasswordInput)
    
    
    class Meta:
        model = get_user_model()
        fields = ('username', 'email', 'password', 'password2', 'first_name', 'last_name')
        
        
        def clean_password2(self):
            cd = self.cleaned_data
            if cd['password']!= cd['password2']:
                raise forms.ValidationError("Passwords don't match")
            return cd['password']
        def clean_email(self):
            email = self.cleaned_data['email']
            if get_user_model().objects.filter(email=email).exists():
                raise forms.ValidationError('Bunday Email mavjud emas')            
            
            return email
        
        

class UserPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(label="Старый пароль", widget=forms.PasswordInput)
    new_password1 = forms.CharField(label="Новый пароль", widget=forms.PasswordInput)
    new_password2 = forms.CharField(label="Подтвердите новый пароль", widget=forms.PasswordInput)
    
    
    
class ProfileForm(forms.ModelForm):
    first_name = forms.CharField(label="First Name")
    first_name = forms.CharField(label="Last Name")
    email = forms.CharField(label="Email")
    username = forms.CharField(label="Username", disabled=True)
    
    class Meta:
        model = get_user_model()
        fields = ('first_name', 'last_name', 'username', 'email')