from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from myapp.models import Profile, PlasticListing, Category


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

class ContactForm(forms.Form):
    first_name = forms.CharField(max_length=100, required=True)
    last_name = forms.CharField(max_length=100, required=True)
    email = forms.EmailField(required=True)
    phone_number = forms.CharField(max_length=20, required=True)
    contact_method = forms.ChoiceField(choices=[('email', 'Email'), ('phone', 'Phone')], required=True)
    country_region = forms.CharField(max_length=100, required=True)
    postal_code = forms.CharField(max_length=20, required=True)
    company_name = forms.CharField(max_length=100, required=True)
    buy_or_sell = forms.ChoiceField(choices=[('buy', 'Buy'), ('sell', 'Sell')], required=True)
    enquiry = forms.CharField(widget=forms.Textarea, required=False)

class CategoryPlasticListingForm(forms.ModelForm):
    class Meta:
        model = PlasticListing
        fields = ['category', 'quantity', 'price', 'description']

    def __init__(self, *args, **kwargs):
        category = kwargs.pop('category', None)
        super().__init__(*args, **kwargs)
        if category:
            self.fields['category'].widget = forms.HiddenInput()
            self.initial['category'] = category


class MarketPlaceFilterForm(forms.Form):
    seller = forms.CharField(required=False, label='Seller')
    min_price = forms.DecimalField(required=False, min_value=0, label='Min Price')
    max_price = forms.DecimalField(required=False, min_value=0, label='Max Price')
    category = forms.ModelChoiceField(queryset=Category.objects.all(), required=False, label='Category')
    sort_by_date = forms.ChoiceField(choices=[('asc', 'Ascending'), ('desc', 'Descending')], required=False, label='Sort by Date')



class PlasticListingForm(forms.ModelForm):
    class Meta:
        model = PlasticListing
        fields = ['category', 'quantity', 'price', 'description', 'images']

    category = forms.ModelChoiceField(queryset=Category.objects.all(), required=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].queryset = Category.objects.all()


