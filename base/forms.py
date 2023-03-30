from django.forms import ModelForm
from django import forms

from .models import Room, Topic

class RoomForm(ModelForm):
    class Meta:
        # here I specify the Room class from 
        # models.py as it is imported 
        model = Room
        # fields = ['name', 'body']
        fields = '__all__'
        exclude = [ 'counsellors']
        # exclude command helps you to get rid of host and counsellors option from create new room option and automatically updates it
    
    description = forms.CharField(widget=forms.TextInput(attrs={'size': '200'}))
    summary = forms.CharField(widget=forms.TextInput(attrs={'size': '200'}))
    recoTest = forms.CharField(widget=forms.TextInput(attrs={'size': '100'}))
    recoUniv = forms.CharField(widget=forms.TextInput(attrs={'size': '100'}))
    subjects = forms.CharField(widget=forms.TextInput(attrs={'size': '80'}))
    dreamCareer = forms.CharField(widget=forms.TextInput(attrs={'size': '50'}))
    majorPlan = forms.CharField(widget=forms.TextInput(attrs={'size': '50'}))
    emailID = forms.CharField(widget=forms.TextInput(attrs={'size': '20'}))
    contactID = forms.CharField(widget=forms.TextInput(attrs={'size': '20'}))



class TopicForm(ModelForm):
    class Meta:
        model = Topic
        fields = '__all__'

