from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User, Application, Review
import re

class RegisterForm(UserCreationForm):
    # Добавляем аргумент label для кастомных полей
    full_name = forms.CharField(label="ФИО", max_length=200, widget=forms.TextInput(attrs={'autocomplete': 'name'}))
    phone = forms.CharField(label="Телефон", max_length=20, widget=forms.TextInput(attrs={'autocomplete': 'tel'}))
    email = forms.EmailField(label="Электронная почта", widget=forms.EmailInput(attrs={'autocomplete': 'email'}))

    class Meta:
        model = User
        fields = ('username', 'full_name', 'phone', 'email')
        # Для полей из модели (username) используем словарь labels
        labels = {
            'username': 'Логин',
        }
        widgets = {
            'username': forms.TextInput(attrs={'autocomplete': 'username'}),
        }

    def clean_username(self):
        username = self.cleaned_data['username']
        if not re.match(r'^[A-Za-z0-9]{6,}$', username):
            raise forms.ValidationError('Логин: латиница и цифры, не менее 6 символов')
        return username

    def clean_full_name(self):
        full_name = self.cleaned_data['full_name']
        if not re.match(r'^[А-ЯЁа-яё\s]+$', full_name):
            raise forms.ValidationError('ФИО: только кириллица и пробелы')
        return full_name

    def clean_phone(self):
        phone = self.cleaned_data['phone']
        if not re.match(r'^8\(\d{3}\)\d{3}-\d{2}-\d{2}$', phone):
            raise forms.ValidationError('Телефон: формат 8(XXX)XXX-XX-XX')
        return phone

class LoginForm(AuthenticationForm):
    # Перевод для формы входа
    username = forms.CharField(label="Логин", widget=forms.TextInput(attrs={'autocomplete': 'username'}))
    password = forms.CharField(label="Пароль", widget=forms.PasswordInput(attrs={'autocomplete': 'current-password'}))


class ApplicationForm(forms.ModelForm):
    start_date = forms.DateField(label="Дата начала", widget=forms.DateInput(attrs={'type':'date'}))
    class Meta:
        model = Application
        fields = ('course_name','start_date','payment_method')
        labels = {
            'course_name': 'Название курса',
            'payment_method': 'Способ оплаты',
        }

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ('text',)
        labels = {
            'text': 'Ваш отзыв',
        }
        widgets = {'text': forms.Textarea(attrs={'rows':3})}
