from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from tennis.forms import LoginForm

# Create your views here.
def home(request):
	return render(request,'tennis/home.html',locals())

def sponsors(request):
	return render(request,'tennis/sponsors.html',locals())

def contact(request):
	return render(request,'tennis/contact.html',locals())

def connect(request):
	if request.method == "POST":
		#Recuperation des donnees
		username = request.POST['username']
		password = request.POST['password']

		#check email
		if username=="":
			error = "Veuillez entrer un nom d'utilisateur valide !"
			return render(request,'tennis/login.html',locals())
		
		#check password
		if password=="":
			error = "Veuillez entrer un mot de passe !"
			return render(request,'tennis/login.html',locals())

		#Connection	
		user = authenticate(username=username, password=password)
		#Si l'utilisateur existe et qu'il est actif on le connecte sinon on affiche un message d'erreur
		if user is not None:
			if user.is_active:
				login(request, user)
				return redirect(reverse(home))
			else:
				error="Ce compte a été désactivé !"
				return render(request,'tennis/login.html',locals())
		else:
			#invalide login
			error = "Nom d'utilisateur ou mot de passe non conforme !"
			return render(request,'tennis/login.html',locals())
	if request.user.is_authenticated():
		return redirect(reverse(home))
	return render(request,'tennis/login.html',locals())

def deconnect(request):
	logout(request)
	return redirect(reverse(home))

def username_present(username):
	if User.objects.filter(username=username).exists():
		return True

	return False

def email_present(email):
    if User.objects.filter(email=email).exists():
        return True

    return False

def register(request):
	if request.method == "POST":

		#Recuperation des donnees
		username = request.POST['username']
		password = request.POST['password']
		firstname = request.POST['firstname']
		lastname = request.POST['lastname']
		email = request.POST['email']
		tel = request.POST['tel']
		gsm = request.POST['gsm']
		fax = request.POST['fax']
		title = request.POST['title']
		street = request.POST['street']
		number = request.POST['number']
		locality = request.POST['locality']
		postalcode = request.POST['postalcode']
		birthdate = request.POST['birthdate']
		classement = request.POST['classement']
		

		#participated = request.POST['participated']


		#check champs
		if (username=="" or password=="" or firstname=="" or lastname=="" or email=="" or (tel=="" 
		and gsm=="") or street=="" or number=="" or locality=="" or postalcode=="" or birthdate==""):
			error = "Veuillez remplir tous les champs obligatoires !"
			return render(request,'tennis/register.html',locals())

		#Check username et email already taken
		if(username_present(username)):
			error = "Cet nom d'utilisateur n'est plus disponible !"
			return render(request,'tennis/register.html',locals())

		if(email_present(email)):
			error = "Un compte avec cette addresse email existe déjà !"
			return render(request,'tennis/register.html',locals())

		#check username length
		if(len(username) < 2):
			error = "Votre nom d'utilisateur doit contenir au moins 3 caractères"
			return render(request,'tennis/register.html',locals())

		#check password length
		if(len(password) < 2):
			error = "Votre mot de passe doit contenir au moins 3 caractères"
			return render(request,'tennis/register.html',locals())

		#Check numero de tel addresse et email valide TODO



		#Account creation & redirect
		
	if request.user.is_authenticated():
		return redirect(reverse(home))
	return render(request,'tennis/register.html',locals())

def recover(request):
	return render(request,'tennis/recover.html',locals())