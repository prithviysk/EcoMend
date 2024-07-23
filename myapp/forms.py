from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from myapp.models import Profile


class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)
    contact_number = forms.CharField(max_length=20, required=False)
    company_name = forms.CharField(max_length=255, required=False)  # Added field

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'contact_number', 'company_name')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            Profile.objects.update_or_create(
                user=user,
                defaults={
                    'contact_number': self.cleaned_data.get('contact_number'),
                    'company_name': self.cleaned_data.get('company_name'),
                }
            )
        return user

class ProfileUpdateForm(forms.ModelForm):
    username = forms.CharField(max_length=150, required=True, label='Username')
    email = forms.EmailField(required=True, label='Email')

    class Meta:
        model = Profile
        fields = ['username', 'email', 'address', 'contact_number', 'company_name']

    def __init__(self, *args, **kwargs):
        super(ProfileUpdateForm, self).__init__(*args, **kwargs)
        if self.instance and self.instance.user:
            self.fields['username'].initial = self.instance.user.username
            self.fields['email'].initial = self.instance.user.email

    def save(self, commit=True):
        profile = super(ProfileUpdateForm, self).save(commit=False)
        user = profile.user
        user.username = self.cleaned_data['username']
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            profile.save()
        return profile