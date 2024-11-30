from django.forms import ModelForm
from .models import Room, Company
from django import forms
from django.contrib.auth.models import User

class RoomForm(ModelForm):
    class Meta:
        model = Room
        fields = '__all__'  # можно использовать лист типа ['name', 'body']

class CompanyRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    company_name = forms.CharField(max_length=255)

    class Meta:
        model = User
        fields = ['username', 'password', 'email']  # Не забудьте добавить company_name в клиентскую часть.

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
            # Сохраняем объект Company
            company = Company.objects.create(
                user=user,
                company_name=self.cleaned_data.get('company_name'),  # Добавьте получение name туда.
                email=self.cleaned_data['email']  # Не забывайте устанавливать email.
            )
        return user
