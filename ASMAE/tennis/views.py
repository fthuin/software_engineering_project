from django.shortcuts import render

# Create your views here.
def home(request):
	#return render(request, 'tennis/home.html')
	return render(request,'tennis/home.html',locals())