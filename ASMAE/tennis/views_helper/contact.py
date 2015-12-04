# /usr/bin/env python
# coding: utf8

from django.shortcuts import render
from tennis.mail import send_contact_mail

def view(request):
    if request.method == "POST":
        if request.POST['action'] == "sendConcactMail":
            subject = request.POST['subject']
            email = request.POST['email']
            message = request.POST['message']
            if send_contact_mail(email, subject, message):
                successSendMail = u"Votre message a bien été envoyé"
            else:
                echecSendMail = u"Une erreur s'est produite lors de l'envoi de votre message,\nle problème a été signalé au staff et sera résolu dans les plus bref délais. Nous sommes désolés, réessayez dans quelques heures"
    return render(request, 'contact.html', locals())
