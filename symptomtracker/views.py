from django.shortcuts import render

# Create your views here.

def home(request):
	return render(request, 'home.html')

def tracker(request):
	return render(request, 'symptomtracker/tracker.html')