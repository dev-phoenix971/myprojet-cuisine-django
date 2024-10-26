from django.shortcuts import render, HttpResponseRedirect, redirect
from django.forms import ModelForm
from .models import Contact
from django.urls import reverse, reverse_lazy
from .forms import ContactForm
from django.http import HttpResponse
from django.core.mail import EmailMessage, send_mail
from django.conf import settings
from django.contrib import messages


# def contact(request):
#     if request.method == 'POST':
#         form = ContactForm(request.POST)
#         if form.is_valid():
#             firstname = form.cleaned_data['firstname']
#             lastname = form.cleaned_data['lastname']
#             email = form.cleaned_data['email']
#             message = form.cleaned_data['message']


#             EmailMessage(
#                'Contact Form Submission from {}'.format(firstname),
#                message,
#                'form-response@example.com', # Send from (your website)
#                ['JohnDoe@gmail.com'], # Send to (your admin email)
#                [],
#                reply_to=[email] # Email from the form to get back to
#             ).send()

#             return redirect('success')
#     else:
#         form = ContactForm()
#     return render(request, 'contact/contact.html', {'form': form})



def contact_view(request):
    form = ContactForm()
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            firstname = form.cleaned_data['firstname']
            lastname = form.cleaned_data['lastname']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']
            titre = f'Cuisine Antillaise | {firstname} {lastname} - {email}'
            send_mail(titre, message, 'david.accipe@gmail.com', ['contact@macuisineantillaise.com'])

            
        return HttpResponseRedirect(reverse('contact:remerciements'))
    return render(request, 'contact/contact.html', {'form': form})

def remerciements_view(request):
    return render(request, 'contact/remerciements.html')
    # return HttpResponse('Merci de nous avoir contacté')