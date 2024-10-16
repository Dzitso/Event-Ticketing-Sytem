from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Attendee, CustomUser, Event, Booking, Organizer

class RegisterAttendeeForm(UserCreationForm):
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Password", widget=forms.PasswordInput)
    first_name = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}))
    last_name = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}))
    email = forms.EmailField(label="", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Email Address'}))
    phone_number = forms.CharField(label="", required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone Number'}))

    class Meta:
        model = CustomUser
        fields = ('username', 'first_name', 'last_name', 'phone_number', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super(RegisterAttendeeForm, self).__init__(*args, **kwargs)
        # Customize form fields...

    def save(self, commit=True):
        user = super().save(commit=False)
        user.user_type = 'attendee'
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
            attendee = Attendee.objects.create(
                user=user,
                phone_number=self.cleaned_data['phone_number']
            )
            attendee.save()
        return user

class RegisterOrganizerForm(UserCreationForm):
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Password", widget=forms.PasswordInput)
    first_name = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}))
    last_name = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}))
    email = forms.EmailField(label="", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Email Address'}))
    phone_number = forms.CharField(label="", required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone Number'}))

    class Meta:
        model = CustomUser
        fields = ('username', 'first_name', 'last_name', 'phone_number', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super(RegisterOrganizerForm, self).__init__(*args, **kwargs)
        # Customize form fields...

    def save(self, commit=True):
        user = super().save(commit=False)
        user.user_type = 'organizer'
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
            organizer = Organizer.objects.create(
                user=user,
                phone_number=self.cleaned_data['phone_number']
            )
            organizer.save()
        return user

class LoginForm(AuthenticationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'password')

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['title', 'venue', 'date', 'time', 'price', 'info', 'category', 'picture']

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['payment_method']