from django.shortcuts import render, redirect

from django.contrib.auth import get_user_model
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
			password = request.POST.get('password')

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
		User = get_user_model()
		users = User.objects.all()

		if request.method == 'POST':
			for thisuser in users:
				if thisuser.username in request.POST:
					if thisuser.is_staff:
						if (request.user == thisuser):
							messages.info(request, "You can't remove your own privileges!")
						else:
							thisuser.is_staff = False
							thisuser.save()
						break
					else:
						thisuser.is_staff = True
						thisuser.save()
						break
				elif thisuser.username+"adm" in request.POST:
					if thisuser.is_superuser:
						if (request.user == thisuser):
							messages.info(request, "You can't remove your own privileges!")
						else:
							thisuser.is_superuser = False
							thisuser.save()
						break
					else:
						thisuser.is_superuser = True
						thisuser.save()
						break


		newusers = User.objects.all()
		context={'users': newusers}
		return render(request, 'adminpanel.html', context)
	else:
		messages.info(request, 'Access denied!')
		return redirect('home')

def staff_p(request):
	if request.user.is_staff:
		return render(request, 'staffpanel.html')
	else:
		messages.info(request, 'Access denied!')
		return redirect('home')