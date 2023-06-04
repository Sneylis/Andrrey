from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import Unit, Profile, Group, Category
from django.contrib.auth.forms import SetPasswordForm
from captcha.fields import CaptchaField

class SearchForm(forms.Form):
    query = forms.CharField(label='поиск')


class UserPasswordChangeForm(SetPasswordForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': 'form-control',
                'autocomplete': 'off'
            })

class UnitForm(forms.ModelForm):
    title = forms.CharField(label='Название')
    about = forms.CharField(label='Описание')
    price = forms.IntegerField(label='Цена')
    characters = forms.CharField(label='Описание')
    photo = forms.ImageField(label='фото')

    class Meta:
        model = Unit
        fields = ['title','about','characters','price','photo','cat']
        widjets = {
            'title': forms.TextInput(attrs={'class': 'form-input'}),
            'about': forms.Textarea(attrs={'class': 'form-input'}),
            'characters': forms.Textarea(attrs={'class': 'form-input'}),
        }

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['avatar','birth']
        widjets = {

        }


class RegisterUserForm(UserCreationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-input'}))
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'class': 'form-input'}))
    first_name = forms.CharField(label="Имя", widget=forms.TextInput(attrs={'class': 'form-input'}))
    last_name = forms.CharField(label="Фамилия", widget=forms.TextInput(attrs={'class': 'form-input'}))
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    password2 = forms.CharField(label='Повтор пароля', widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    captcha = CaptchaField()
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')
        widjets = {
            'username': forms.TextInput(attrs={'class': 'form-input'}),
            'first_name': forms.TextInput(attrs={'class': 'form-input'}),
            'last_name': forms.TextInput(attrs={'class': 'form-input'}),
            'email': forms.TextInput(attrs={'class': 'form-input'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-input'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-input'}),
        }

    # def clean(self):
    #     cleaned_data = super().clean(self)
    #     if User.objects.filter(email=cleaned_data.get('email')).exists():
    #         self.fields.add_error('email', "Эта почта уже зарегестрированна")
    #     return cleaned_data

class LoginForm(forms.Form):
    username = forms.CharField(label=u'Имя пользователя')
    password = forms.CharField(
        label=("Пароль"),
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "current-password"}),
    )
    captcha = CaptchaField()

class GroupForm(forms.ModelForm):
    gr = forms.CharField(label='Группа')

    class Meta:
        model = Group
        fields = ['gr']

class CatForm(forms.ModelForm):
    cat = forms.CharField(label='Категория')

    class Meta:
        model = Category
        fields = '__all__'