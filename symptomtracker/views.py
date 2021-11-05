from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import  UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import CreateUserForm
from decouple import config
import dateutil.tz as dtz
from datetime import *
import pytz
import json

#custom py files
from . import alg
from . import mongoform

#for pdf coversion
from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa

#Creating a pdf
def render_to_pdf(template_src, context_data={}):
	template = get_template(template_src)
	html = template.render(context_data)
	result = BytesIO()
	pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
	if not pdf.err:
		return HttpResponse(result.getvalue(), content_type='application/pdf')
	return 0

#Home page
def home(request):
	contArr = mongoform.getContacts()
	if contArr == 0:
		messages.info(request, "Database Error: Failed to get some data from database.")
	context = {"contacts":contArr}
	return render(request, 'home.html', context)

#Show profile page
def profile(request):
	if request.user.is_authenticated:
		if (request.user.first_name == ""):
			return redirect('edit_profile')
		edit_data = mongoform.get_profile(request.user.id) 
		if (edit_data == 0):
			messages.info(request,"Database Error: Failed to retrive data from database.")
			return redirect('home')
		context = {'editdata' : edit_data}
		return render(request, 'symptomtracker/profile.html', context)
	messages.info(request, 'Please login to access the profile')
	return redirect('home')
	
#Registration page
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
			return redirect('edit_profile')
		messages.info(request, 'Please check the errors')
	context = {'form':form}
	return render(request, 'accounts/register.html', context)
	
#Login page
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

#Logging out the current user
def logoutuser(request):
	logout(request)
	messages.info(request, 'Successfully logged out.')
	return redirect('home')

#Edit profile page
def edit_profile(request):
	if request.user.is_authenticated:
		if request.method == 'POST':
			newdata = [] #Get form data into an array
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
			db_errors = mongoform.edit_user(request.user.id, newdata)
			if(db_errors==0):
				if(request.user.first_name == ""):
					messages.info(request, 'Registration process is complete')
				else:
					messages.info(request, 'Successfully updated the profile')
				this_user = request.user
				this_user.first_name = newdata[0]
				this_user.last_name = newdata[1]
				this_user.save()
			else:
				messages.info(request, "Database Error: Couldn't save data to the database")
			return redirect('home')
		if(request.user.first_name == ""):
			return render(request, 'symptomtracker/edit_profile.html')
		edit_data = mongoform.get_profile(request.user.id) 
		if (edit_data == 0):
			messages.info(request,"Database Error: Failed to retrive data from database.")
			return redirect('home')
		context = {'editdata' : edit_data}
		return render(request, 'symptomtracker/edit_profile.html', context)
	messages.info(request, 'Please login to access!')
	return redirect('home')

#Symptom tracker page
def tracker(request):
	if request.user.is_authenticated:
		if (request.user.first_name == ""):
			return redirect('edit_profile')
		#on post req for ending the current session
		if request.method == 'POST' and 'EndSession' in request.POST:
			timeNow = datetime.now().astimezone(pytz.timezone('Asia/Colombo'))
			date_now = timeNow.strftime('%d-%m-%Y')
			end_err = mongoform.endSession(request.user.id, date_now)
			if end_err != 0:
				messages.info(request, "Database Error: Couldn't access the database")
			return redirect('tracker')
		#on post req for printing a pdf report
		if request.method == 'POST' and 'printReport' in request.POST:
			dataset = mongoform.allSessions(request.user.id)
			profile = mongoform.get_profile(request.user.id) 
			if (dataset == -1 or profile == 0):
				messages.info(request, "Database Error: Failed to retrive data from database.")
				return redirect('home')
			context = {"sessions" : dataset, "profile" : profile}
			pdf = render_to_pdf('symptomtracker/printReport.html', context)
			response = HttpResponse(pdf, content_type='application/pdf')
			filename = "Covid_Status_Report_of_%s.pdf" %(request.user.first_name)
			content = "attachment; filename=%s" %(filename)
			response['Content-Disposition'] = content
			return response
		dataset = mongoform.allSessions(request.user.id)
		profile = mongoform.get_profile(request.user.id) 
		if (dataset == -1 or profile == 0):
			messages.info(request, "Database Error: Failed to retrive data from database.")
			return redirect('home')
		context = {"sessions" : dataset, "profile" : profile}
		return render(request, 'symptomtracker/tracker.html', context)
	messages.info(request, 'Please login to use the symptom tracker')
	return redirect('home')

#Symptom insertion page
def daily_session(request):
	if request.user.is_authenticated:
		if (request.user.first_name == ""):
			return redirect('edit_profile')
		if request.method == 'POST':
			timeNow = datetime.now().astimezone(pytz.timezone('Asia/Colombo'))
			symptom = [] #Getting symptom data into an array
			symptom.append(request.user.id)									#id
			symptom.append(timeNow.strftime('%d-%m-%Y')) 					#0
			symptom.append(timeNow.strftime('%H:%M'))						#1
			symptom.append(float(request.POST.get('ColdSlider')))			#2
			symptom.append(float(request.POST.get('JointPainSlider')))		#3
			symptom.append(float(request.POST.get('WeakSlider')))			#4
			symptom.append(float(request.POST.get('AppSlider')))			#5
			symptom.append(float(request.POST.get('AbdPainSlider')))		#6
			symptom.append(float(request.POST.get('ThroatSlider')))			#7
			symptom.append(float(request.POST.get('headacheSlider')))		#8											
			symptom.append(float(request.POST.get('bTempInput')))			#9	
			symptom.append(float(request.POST.get('drychSlider')))			#10
			symptom.append(float(request.POST.get('DyspSlider')))			#11
			symptom.append(float(request.POST.get('NausSlider')))			#12
			symptom.append(float(request.POST.get('vomitSlider')))			#13
			symptom.append(float(request.POST.get('DiarSlider')))			#14
			#Calling the analysis alg
			analysis_err = alg.symptomAnalysis(symptom)
			if analysis_err != 0:
				messages.info(request, "Database Error: Couldn't save data to the database")
			return redirect('tracker')
		#Getting an array of days of the last session
		days_arr = mongoform.lastSession(request.user.id)
		if days_arr == -1:
			messages.info(request, "Database Error: Couldn't access the database. Please try again later.")
			return redirect('tracker')
		elif days_arr == 0:
			return render(request, 'symptomtracker/daily_session.html')
		else:
			#Checking the time of last session and time for the next session
			timeNow = datetime.now().astimezone(pytz.timezone('Asia/Colombo'))
			today = timeNow.strftime('%d-%m-%Y')
			last_day = days_arr[-1]['Input_Data'][0]
			last_time = days_arr[-1]['Input_Data'][1]
			if len(days_arr)<2 or last_day != days_arr[-2]['Input_Data'][0] or last_day != today:
				if last_day == today:
					timeNow = datetime.now().astimezone(pytz.timezone('Asia/Colombo'))
					time_now = timeNow.strftime('%H:%M')
					time_dif = datetime.strptime(time_now, '%H:%M') - datetime.strptime(last_time, '%H:%M')
					time_dif_in_time = (datetime.min + time_dif).time()
					if time_dif_in_time < datetime.strptime('6:00','%H:%M').time():
						wait_time = datetime.strptime('6:00','%H:%M') - time_dif
						wait_time = wait_time.time()
						msg = "You have to wait "+str(wait_time.hour)+" hours and "+str(wait_time.minute)+" minutes for the next session."
						messages.info(request, msg)
						return redirect('tracker')
				return render(request, 'symptomtracker/daily_session.html')
			messages.info(request, "You have completed two sessions for today! Please enter your symptoms again tomorrow.")	
			return redirect('tracker')
	messages.info(request, 'Please login to use the symptom tracker')
	return redirect('home')
	

#Admin panel page
def admin_p(request):
	if request.user.is_superuser:
		User = get_user_model()
		users = User.objects.all()
		if request.method == 'POST': #to ensure the system will have at least 1 admin
			for thisuser in users:
				#Changing admin privilages
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

#Staff panel page
def staff_p(request):
	if request.user.is_staff:
		#Updating contact data
		if request.method == 'POST' and 'update' in request.POST:
			data = request.POST.get('updateData')
			cont_data = json.loads(data, strict=False)
			if mongoform.addContacts(cont_data) == -1:
				messages.info(request, "Database Error: Failed to access the database.")
		#Updating location data
		if request.method == 'POST' and 'updateLoc' in request.POST:
			data = request.POST.get('updateDataLoc')
			loc_data = json.loads(data, strict=False)
			if mongoform.addLoc(loc_data) == -1:
				messages.info(request, "Database Error: Failed to access the database.")
		#Deleting contact data
		if request.method == 'POST' and 'delete' in request.POST:
			data = request.POST.get('deleteData')
			if mongoform.delContacts(data) == -1:
				messages.info(request, "Database Error: Failed to delete.")
		#Deleting location data
		if request.method == 'POST' and 'deleteLoc' in request.POST:
			data = request.POST.get('deleteDataLoc')
			if mongoform.delLoc(data) == -1:
				messages.info(request, "Database Error: Failed to delete.")

		#Displaying contact and location data in staff panel
		contArr = mongoform.getContacts()
		mapArr = mongoform.getMap()

		if contArr == 0 or mapArr == 0:
			messages.info(request, "Database Error: Failed to get some data from database.")

		context = {
			"contacts": contArr,
			"locations":mapArr
		}
		return render(request, 'staffpanel.html', context)
	messages.info(request, 'Access denied!')
	return redirect('home')