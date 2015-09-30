from django.shortcuts import render

# Create your views here.
def home(request):
	return render(request,'tennis/home.html',locals())

def login(request):
	return render(request,'tennis/login.html',locals())

def register(request):
	return render(request,'tennis/register.html',locals())

def joueurs(request):
	return render(request,'tennis/joueurs.html',locals())