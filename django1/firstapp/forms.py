from django import forms
from django.forms import ModelForm
from .models import Venue, Event

# create a new venue form
class VenueForm(ModelForm):
    class Meta:
        model = Venue
        #fields = "__all__"
        fields = ('name', 'address', 'zip_code', 'phone', 'web', 'email_address', 'capacity')
        labels = {
            'name': '',
            'address': '',
            'zip_code': '',
            'phone': '',
            'web': '',
            'email_address': '',
            'capacity': ''
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Venue Name'}),
            'address': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Addree'}),
            'zip_code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Zip Code'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone Number'}),
            'web': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Website'}),
            'email_address': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email Address'}),
            'capacity': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'capacity'}),
        }

# create a new event form
class EventForm(ModelForm):
    class Meta:
        model = Event
        #fields = "__all__"
        fields = ('name', 'event_date', 'venue', 'manager', 'attendees', 'description',)
        labels = {
            'name': '',
            'event_date': '',
            'venue': 'Venue',
            'manager': 'Manager',
            'attendees': 'Attendees',
            'description': ''
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Event Name'}),
            'event_date': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Event Date: YYY-MM-DD HH-MM-SS'}),
            'venue': forms.Select(attrs={'class': 'form-select', 'placeholder': 'Venue'}),
            'manager': forms.Select(attrs={'class': 'form-select', 'placeholder': 'Manager'}),
            'attendees': forms.SelectMultiple(attrs={'class': 'form-select', 'placeholder': 'Attendees'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Description'}),
        }