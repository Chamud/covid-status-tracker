from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import  UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import CreateUserForm
from decouple import config

#custom py files
from . import alg
from . import mongoform


def home(request):
	return render(request, 'home.html')

def register(request):
	form = CreateUserForm()
	if request.method == 'POST':
		form = CreateUserForm(request.POST)
		if form.is_valid():
			new_user = form.save()
			username = form.cleaned_data.get('username')
			User = get_user_model()
			user = User.objects.get(username=username) #to create a record in mongodb
			db_errors = mongoform.pre_reg_new_user(user)
			if(db_errors != 0):
				messages.info(request, "Database Error: Couldn't save data to the database")
				return redirect('home')
			messages.info(request, 'An account was created for ' + new_user.username)
			login(request, new_user)
			return redirect('new_profile')
		messages.info(request, 'Please check th errors')
	context = {'form':form}
	return render(request, 'accounts/register.html', context)
	

def loginuser(request):
	if request.user.is_authenticated:
		messages.info(request, 'You are already logged in as ' + request.user.username)
		return redirect('home')
	if request.method == 'POST':
		username = request.POST.get('username')
		password = request.POST.get('password')
		user = authenticate(request, username=username, password=password)
		if user is not None:
			login(request, user)
			return redirect('home')
		messages.info(request, 'Username OR password is incorrect')
	return render(request, 'accounts/login.html')

def logoutuser(request):
	logout(request)
	messages.info(request, 'Successfully logged out.')
	return redirect('home')

def new_profile(request):
	if request.user.is_authenticated:
		if (request.user.first_name != ""):
			messages.info(request, 'You have already completed registration')
			return redirect('home')
		if request.method == 'POST':
			newdata = []
			newdata.append(request.POST.get('firstname'))
			newdata.append(request.POST.get('lastname'))
			newdata.append(request.POST.get('IDvalue'))
			newdata.append(request.POST.get('idtype'))
			newdata.append(request.POST.get('homeadd'))
			newdata.append(request.POST.get('dob'))
			newdata.append(request.POST.get('phone'))
			newdata.append(request.POST.get('vaccinated'))
			newdata.append(request.POST.get('covidstatus'))
			newdata.append(request.POST.get('carddis'))
			newdata.append(request.POST.get('diabdis'))
			newdata.append(request.POST.get('crddis'))
			newdata.append(request.POST.get('cancdis'))
			newdata.append(request.POST.get('othdis'))
			db_errors = mongoform.reg_new_user(request.user.id, newdata)
			if(db_errors==0):
				messages.info(request, 'Registration process is complete')
				this_user = request.user
				this_user.first_name = newdata[0]
				this_user.last_name = newdata[1]
				this_user.save()
			else:
				messages.info(request, "Database Error: Couldn't save data to the database")
			return redirect('home')
		return render(request, 'symptomtracker/new_profile.html')
	messages.info(request, 'Please login to access!')
	return redirect('home')

def profile(request):
	if request.user.is_authenticated:
		if (request.user.first_name == ""):
			return redirect('new_profile')
		return render(request, 'symptomtracker/profile.html')
	messages.info(request, 'Please login to access the profile')
	return redirect('home')

def tracker(request):
	if request.user.is_authenticated:
		if (request.user.first_name == ""):
			return redirect('new_profile')
		return render(request, 'symptomtracker/tracker.html')
	messages.info(request, 'Please login to use the symptom tracker')
	return redirect('home')


def admin_p(request):
	if request.user.is_superuser:
		User = get_user_model()
		users = User.objects.all()
		if request.method == 'POST': #to ensure the system will have at least 1 admin
			for thisuser in users:
				if thisuser.username in request.POST:
					if thisuser.is_staff:
						if (request.user == thisuser):
							messages.info(request, "You can't remove your own privileges!")
						else:
							thisuser.is_staff = False
							thisuser.is_superuser = False
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
						thisuser.is_staff = True
						thisuser.save()
						break
		newusers = User.objects.all()
		context={'users': newusers}
		return render(request, 'adminpanel.html', context)
	messages.info(request, 'Access denied!')
	return redirect('home')

def staff_p(request):
	if request.user.is_staff:
		return render(request, 'staffpanel.html')
	messages.info(request, 'Access denied!')
	return redirect('home')