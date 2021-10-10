from django.shortcuts import render, redirect

from django.contrib.auth.forms import  UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from pymongo import MongoClient

from decouple import config

from . import alg

# Create your views here.
from .forms import CreateUserForm

def home(request):
	return render(request, 'home.html')

def register(request):
	form = CreateUserForm()

	if request.method == 'POST':
		form = CreateUserForm(request.POST)
		if form.is_valid():
			form.save()
			user = form.cleaned_data.get('username')
			messages.success(request, 'Account was created for ' + user)
			return redirect('login')
		else:
			messages.info(request, 'Please check th errors')

	context = {'form':form}
	return render(request, 'accounts/register.html', context)
	

def loginuser(request):
	if request.user.is_authenticated:
		messages.info(request, 'You are already logged in as ' + request.user.username)
		return redirect('home')
	else:
		if request.method == 'POST':
			username = request.POST.get('username')
			password =request.POST.get('password')

			user = authenticate(request, username=username, password=password)

			if user is not None:
				login(request, user)
				return redirect('home')
			else:
				messages.info(request, 'Username OR password is incorrect')

	return render(request, 'accounts/login.html')

def logoutuser(request):
	logout(request)
	messages.info(request, 'Successfully logged out.')
	return redirect('home')


@login_required(login_url='login')
def tracker(request):
	client = MongoClient(config('DB_CONNECTION'))
	db = client.get_database('CST')
	records = db.UserData
	n = records.count_documents({})
	messages.info(request, 'Number of users = ' + str(n))
	return render(request, 'symptomtracker/tracker.html')


def admin_p(request):
	if request.user.is_superuser:
		return render(request, 'adminpanel.html')
	else:
		messages.info(request, 'Access denied!')
		return redirect('home')

def staff_p(request):
	if request.user.is_staff:
		return render(request, 'staffpanel.html')
	else:
		messages.info(request, 'Access denied!')
		return redirect('home')