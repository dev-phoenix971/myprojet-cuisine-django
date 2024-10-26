from django import forms
from django.contrib.auth.forms import UserCreationForm, ReadOnlyPasswordHashField, PasswordResetForm
from django.contrib.auth import authenticate, get_user_model
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.conf import settings
from django.db.models import Q
from .models import USERNAME_REGEX, Profile
from collections import OrderedDict


User = get_user_model()

class UserLoginForm(forms.Form):
    query = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder':'Your Pseudo or Email'}))
    password = forms.CharField(label='', widget = forms.PasswordInput(attrs={'placeholder':'Password'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if settings.USE_REMEMBER_ME:
            self.fields['remember_me'] = forms.BooleanField(label=('Remember me'), required=False)
    
    def clean(self, *args, **kwargs):
        query = self.cleaned_data.get("query")
        password = self.cleaned_data.get("password")

        user_qs_final = User.objects.filter(
            Q(username__iexact=query)|
            Q(email__iexact=query)
        ).distinct() 
        if not user_qs_final.exists() and user_qs_final.count() != 1:
                raise forms.ValidationError("Invalid crédentials -- user not exist")
        user_obj = user_qs_final.first()
        if not user_obj.check_password(password):
                raise forms.ValidationError("Invalid crédentials -- password invalid")
        if not user_obj.is_active:
                    raise forms.ValidationError("Inactive user. Please verify your email address")
        self.cleaned_data["user_obj"] = user_obj
        return super(UserLoginForm, self).clean(*args, **kwargs)



class CreateNewUser(UserCreationForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    email = forms.EmailField(required=True, label="", widget=forms.TextInput(attrs={'placeholder':'Your Email'}))
    username = forms.CharField(required=True, label="", widget=forms.TextInput(attrs={'placeholder':'Your Username'}))
    password1 = forms.CharField(required=True, label="", widget=forms.PasswordInput(attrs={'placeholder':'Password'}))
    password2 = forms.CharField(
        required=True,
        label="", widget=forms.PasswordInput(attrs={'placeholder':'Password Confirmation'}))
    

    class Meta:
        model = User
        fields = ["username","email", "password1", "password2"]

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        user.is_active = False
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    disabled password hash display field.
    """

    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ["username", "email", "password", "is_staff", "is_active", "is_admin"]


class EditProfileForm(forms.ModelForm):
    date_naissance = forms.DateField(widget=forms.TextInput(attrs={'type':'date',}))
    first_name = forms.CharField(required=False, label="", widget=forms.TextInput(attrs={'placeholder':'Your First name'}))
    last_name = forms.CharField(required=False, label="", widget=forms.TextInput(attrs={'placeholder':'Your Last name'}))
    
    
    class Meta:
        model = Profile
        fields = ["photo", "first_name", "last_name", "date_naissance", "website", "facebook"]



class PhotoForm(forms.ModelForm):
    class Meta :
        model = Profile
        fields = ['photo',]


class SetPasswordForm(forms.Form):
    error_messages = {
        'password_mismatch':("The two password fields didn't match."),
    }
    new_password1 = forms.CharField(label=("New password"),
                                    widget=forms.PasswordInput)
    new_password2 = forms.CharField(label=("New password confirmation"),
                                    widget=forms.PasswordInput)

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(SetPasswordForm, self).__init__(*args, **kwargs)

    def clean_new_password2(self):
        password1 = self.cleaned_data.get('new_password1')
        password2 = self.cleaned_data.get('new_password2')
        if password1 and password2:
            if password1 != password2:
                raise forms.ValidationError(
                    self.error_messages['password_mismatch'],
                    code='password_mismatch',
                )
        return password2

    def save(self, commit=True):
        self.user.set_password(self.cleaned_data['new_password1'])
        if commit:
            self.user.save()
        return self.user

class PasswordChangeForm(SetPasswordForm):
    """
    A form that lets a user change their password by entering their old
    password.
    """
    error_messages = dict(SetPasswordForm.error_messages, **{
        'password_incorrect': ("Your old password was entered incorrectly. "
                                "Please enter it again."),
    })
    old_password = forms.CharField(label=("Old password"),
                                   widget=forms.PasswordInput)

    def clean_old_password(self):
        """
        Validates that the old_password field is correct.
        """
        old_password = self.cleaned_data["old_password"]
        if not self.user.check_password(old_password):
            raise forms.ValidationError(
                self.error_messages['password_incorrect'],
                code='password_incorrect',
            )
        return old_password


PasswordChangeForm.base_fields = OrderedDict(
    (k, PasswordChangeForm.base_fields[k])
    for k in ['old_password', 'new_password1', 'new_password2']
)


class PasswordResetForm(PasswordResetForm):
    def __init__(self, *args, **kwargs):
        super(PasswordResetForm, self).__init__(*args, **kwargs)

    #captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox())