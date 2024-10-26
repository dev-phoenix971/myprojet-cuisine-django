from django import forms
from django.core.validators import EmailValidator
from django_recaptcha.fields import ReCaptchaField 
from django_recaptcha.widgets import ReCaptchaV2Checkbox 
  
  
class ContactForm(forms.Form): 
    firstname = forms.CharField(required=True, label="", widget=forms.TextInput(attrs={'placeholder':'firsname'}))
    lastname = forms.CharField(required=True, label="", widget=forms.TextInput(attrs={'placeholder':'lastname'}))
    email = forms.EmailField(required=True, label="", widget=forms.EmailInput(attrs={'placeholder':'Your Email'}))
    message = forms.CharField(required=True, label="", widget=forms.Textarea(attrs={"row": "100", 'placeholder':'Your Message' }))
    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox) 