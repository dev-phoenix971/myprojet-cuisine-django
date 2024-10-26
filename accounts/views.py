
from typing import Any
from django.contrib.auth import login, logout, get_user_model
from django.http import HttpRequest, HttpResponseRedirect, HttpResponse, HttpResponseBadRequest
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.decorators import login_required
from django.utils.encoding import force_bytes, force_str
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, UpdateView
from .models import MyUser, Profile
from .token import account_activation_token
from .forms import EditProfileForm, SetPasswordForm, PasswordResetForm
from django.db.models import Q
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
import datetime
from blog.models import Blog


User = get_user_model()

from .forms import CreateNewUser, UserLoginForm, PhotoForm



def register(request):
    if request.method == 'POST':
        form = CreateNewUser(request.POST or None)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()

            current_site = get_current_site(request)
            subject = 'Activate your blog account.'
            message = render_to_string('accounts/activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                        subject, message, to=[to_email]
            )
            email.send()
            # return HttpResponse('Please confirm your email address to complete the registration')
            return redirect(reverse('accounts:account_activation_sent'))
    else:
            form = CreateNewUser()
    return render(request=request, template_name='accounts/register.html', context={'title':'Signup Form Here','form': form})


@login_required
def account_activation_sent(request):
    return render(request, 'accounts/activation_sent.html')

def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.profile.signup_confirmation = True
        user.save()
        login(request, user)
        return redirect(reverse('accounts:account_activation_complete'))
    else:
        return HttpResponseBadRequest('Activation link is invalid!')

@login_required
def profile_page(request):
    data = get_object_or_404(Profile, user=request.user)
    blogs = Blog.objects.all()
    post_author = Blog.objects.all()
    context = {'data': data, 'blogs': blogs, 'post_author': post_author}
    
    return render(request, 'accounts/profile.html', context)


@login_required
def account_activation_complete(request):
    return render(request, 'accounts/activation_complete.html') 


def login_view(request, *args, **kwargs):
    form = UserLoginForm(request.POST or None)
    if form.is_valid():
        user_obj = form.cleaned_data.get('user_obj')
        login(request, user_obj)
        return HttpResponseRedirect("/")
    return render(request, "accounts/login.html", context={'title':'Login','form': form})


def logout_view(request):
    logout(request)
    return HttpResponseRedirect("/login")

def activation_sent_view(request):
    return render(request, 'accounts/activation_sent.html')

@login_required
def add_photo(request):
    form= PhotoForm()
    if request.method == 'POST':
        form = PhotoForm(request.POST, request.FILES)
        if form.is_valid():
            user_obj = form.save(commit=False)
            user_obj.user = request.user
            user_obj.save()
            return HttpResponseRedirect(reverse('accounts:profile'))
    return render(request, 'accounts/photo_add.html', context={'form':form})


@login_required
def change_photo(request):
    form= PhotoForm(instance=request.user.profile)
    if request.method == 'POST':
        form = PhotoForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('accounts:profile'))

    return render(request, 'accounts/photo_add.html', context={'form':form})



class CreateProfile(LoginRequiredMixin, CreateView):
    model = Profile
    template_name = 'accounts/create_profile.html'
    fields = ('first_name', 'last_name', 'date_naissance', 'website', 'facebook')




class UpdateProfile(LoginRequiredMixin, UpdateView):
    model = Profile
    template_name = 'accounts/edite_profile.html'
    fields = ('photo', 'first_name', 'last_name', 'date_naissance', 'website', 'facebook')
    

    def form_valid(self, form):
        # profile_obj = form.save(commit=False)
        # profile_obj.user = self.request.user
        # profile_obj.save()
        profile = form.save()
        user = profile.user
        user.photo = form.cleaned_data['photo']
        user.first_name = form.cleaned_data['first_name']
        user.last_name = form.cleaned_data['last_name']
        user.date_naissance = form.cleaned_data['date_naissance']
        user.website = form.cleaned_data['website']
        user.facebook = form.cleaned_data['facebook']
        user.save()
        return HttpResponseRedirect(reverse('accounts:profile'))


def profile_complete(request):
    return render(request, 'accounts/profile_complete.html')

@login_required
def password_change(request):
    user = request.user
    if request.method == 'POST':
        form = SetPasswordForm(user, request.POST)
        if form.is_valid():
            form.save()
            messages.success (request, _("Your password has been changed"))
            return redirect('/accounts/login')
        else:
            for error in list(form.errors.values()):
                messages.error(request, error)

    form = SetPasswordForm(user)
    return render(request, 'accounts/password_reset_confirm.html', {'form': form})



@login_required
def password_reset_request(request):
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            user_email = form.cleaned_data['email']
            associated_user = get_user_model().objects.filter(Q(email=user_email)).first()
            if associated_user:
                subject = _("Password Reset request")
                message = render_to_string('accounts/password_reset_form.html',{
                    'user': associated_user,
                    'domain': get_current_site(request).domain,
                    'uid': urlsafe_base64_encode(force_bytes(associated_user.pk)),
                    'token': account_activation_token.make_token(associated_user),
                    "protocol": 'https' if request.is_secure() else 'http'
                })
                email = EmailMessage(subject, message, to=[associated_user.email])
                if email.send():
                    messages.success(request, _("We've emailed you instructions for setting your password, if an account exists with the email you entered. You should receive them shortly. If you don't receive an email, please make sure you've entered the address you registered with, and check your spam folder.")
                       
                    )
                else:
                    messages.error(request, _("Problem sending reset password email, <b>SERVER PROBLEM</b>"))

            return redirect('home')

        for key, error in list(form.errors.items()):
            if key == 'captcha' and error[0] == 'This field is required.':
                messages.error(request, "You must pass the reCAPTCHA test")
                continue

    form = PasswordResetForm()
    return render(request, "accounts/password_reset.html", context={"form": form}
        )



@login_required
def passwordResetConfirm(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except:
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        if request.method == 'POST':
            form = SetPasswordForm(user, request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, _("Your password has been set. You may go ahead and <b>log in </b> now."))
                return redirect('home')
            else:
                for error in list(form.errors.values()):
                    messages.error(request, error)

        form = SetPasswordForm(user)
        return render(request, 'accounts/password_reset_confirm.html', {'form': form})
    else:
        messages.error(request, "Link is expired")

    messages.error(request, _('Something went wrong, redirecting back to Homepage'))
    return redirect("home")
# ''' def userprofileview(request):
#     if request.method == 'POST':
#         form = EditProfileForm(request.POST, request.FILES)
#         if form.is_valid():
#             pr = UserProfile()
#             pr.user = User.objects.get(id=request.user.id)



@login_required
def password_reset_complete(request):
    return render(request, 'accounts/password_reset_complete.html')




@login_required
def confidentialite(request):
    return render(request, 'accounts/confidentialite.html')