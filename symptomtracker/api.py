from django.templatetags.static import static
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import CreateUserForm
from django.http import JsonResponse
from bson import json_util
from decouple import config
import dateutil.tz as dtz
from datetime import *
import pytz
import json

from django.views.decorators.csrf import csrf_exempt

#custom py files
from . import alg
from . import mongoform

from bson import ObjectId

#To make the ObjectID(id in the mongoDB objects) serializable 
class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)

#list of apis
def apis(request):
	context = {
		"Home": "https://covidstatustracker.herokuapp.com/api/home",
		"Map": "https://covidstatustracker.herokuapp.com/api/map",
		"Tracker": "https://covidstatustracker.herokuapp.com/api/tracker",
		"DailySession": "https://covidstatustracker.herokuapp.com/api/daily_session",
		"Profile": "https://covidstatustracker.herokuapp.com/api/profile",
		"EditProfile": "https://covidstatustracker.herokuapp.com/api/edit_profile",
		"Register": "https://covidstatustracker.herokuapp.com/api/register",
		"Login": "https://covidstatustracker.herokuapp.com/api/login",
		"Logout": "https://covidstatustracker.herokuapp.com/api/logout",
		"AdminPanel": "https://covidstatustracker.herokuapp.com/api/admin_panel",
		"StaffPanel": "https://covidstatustracker.herokuapp.com/api/staff_panel",
	}
	return JsonResponse(context)

#Home api
def home(request):
	userName = request.GET['username']
	password = request.GET['password']
	user = authenticate(request, username=userName, password=password)
	if user is not None:
			login(request, user)
			
	contArr = mongoform.getContacts()
	if contArr == 0:
		messages = "Database Error: Failed to get some data from database"
	else:
		messages = "Success"
	if request.user.is_authenticated:
		userfname = request.user.get_full_name() 
	else:
		userfname = "none"
	data = JSONEncoder().encode(contArr)
	data = json.loads(data)
	url = "https://covidstatustracker.herokuapp.com/static/images/logo.png"
	render = "home"
	context = {"Message": messages, "render": render, "user": userfname, "is_authenticated": request.user.is_authenticated, "is_staff": request.user.is_staff, "is_admin": request.user.is_superuser, "media": url, "contacts": data }
	return JsonResponse(context)

#Show profile api
def profile(request):
	userName = request.GET['username']
	password = request.GET['password']
	user = authenticate(request, username=userName, password=password)
	if user is not None:
			login(request, user)

	if request.user.is_authenticated:
		if (request.user.first_name == ""):
			messages = "Complete registration."
			render = "edit_profile"
			context = {"Message": messages, "render": render}
			return JsonResponse(context)
		edit_data = mongoform.get_profile(request.user.id) 
		if (edit_data == 0):
			messages = "Database Error: Failed to retrive data from database."
			render = "home"
			context = {"Message": messages, "render": render}
			return JsonResponse(context)
		acc_data = {"Account_ID": request.user.id, "Username": request.user.username, "Email": request.user.email}
		messages = "Success"
		render = "profile"
		context = {"Message": messages, "render": render, "account_data": acc_data, "user_data" : edit_data}
		return JsonResponse(context)
	messages = "Login to access the profile"
	render = "home"
	context = {"Message": messages, "render": render}
	return JsonResponse(context)
	
#Registration api
@csrf_exempt
def register(request):
	if request.method == 'POST': #post data : username, email, password1, password2
		form = CreateUserForm(request.POST)
		if form.is_valid():
			new_user = form.save()
			username = form.cleaned_data.get('username')
			User = get_user_model()
			user = User.objects.get(username=username) #to create a record in mongodb
			db_errors = mongoform.pre_reg_new_user(user)
			if(db_errors != 0):
				messages = "Database Error: Couldn't save data to the database"
				render = "home"
				context = {"Message": messages, "render": render}
				return JsonResponse(context)
			messages = 'Success'
			login(request, new_user)
			render = "edit_profile"
			context = {"Message": messages, "render": render}
			return JsonResponse(context)
		messages = "Please check for the errors"
		render = "register"
		context = {"Message": messages, "render": render, "errors": form.errors.as_text()}
		return JsonResponse(context)
	messages = "Success"
	render = "register"
	context = {"Message": messages, "render": render}
	return JsonResponse(context)

#Login api
@csrf_exempt
def loginuser(request):
	if request.user.is_authenticated:
		messages = 'You are already logged in'
		render = "home"
		context = {"Message": messages, "render": render}
		return JsonResponse(context)
	if request.method == 'POST':
		username = request.POST.get('username')
		password = request.POST.get('password')
		user = authenticate(request, username=username, password=password)
		if user is not None:
			login(request, user)
			messages = "Success"
			render = "home"
			context = {"Message": messages, "render": render}
			return JsonResponse(context)
		messages = 'Username OR password is incorrect'
		render = "login"
		context = {"Message": messages, "render": render}
		return JsonResponse(context)
	messages = "Success"
	render = "login"
	context = {"Message": messages, "render": render}
	return JsonResponse(context)

#Logout api
def logoutuser(request):
	logout(request)
	messages = "Success"
	render = "home"
	context = {"Message": messages, "render": render}
	return JsonResponse(context)

#Edit profile api
@csrf_exempt
def edit_profile(request):
	userName = request.GET['username']
	password = request.GET['password']
	user = authenticate(request, username=userName, password=password)
	if user is not None:
			login(request, user)
			
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
				this_user = request.user
				this_user.first_name = newdata[0]
				this_user.last_name = newdata[1]
				this_user.save()
				messages = "Success"
				render = "home"
				context = {"Message": messages, "render": render}
				return JsonResponse(context)
			else:
				messages = "Database Error: Couldn't save data to the database"
				render = "home"
				context = {"Message": messages, "render": render}
				return JsonResponse(context)
		if(request.user.first_name == ""):
			messages = "Success"
			render = "edit_profile"
			context = {"Message": messages, "render": render}
			return JsonResponse(context)
		edit_data = mongoform.get_profile(request.user.id) 
		if (edit_data == 0):
			messages = "Database Error: Failed to retrive data from database."
			render = "home"
			context = {"Message": messages, "render": render}
			return JsonResponse(context)
		messages = "Success"
		render = "edit_profile"
		context = { "Message": messages, "render": render, 'profile_data' : edit_data}
		return JsonResponse(context)
	messages = "Login to access"
	render = "home"
	context = {"Message": messages, "render": render}
	return JsonResponse(context)

#printing pdf
@csrf_exempt
def printpdf(request):
	userName = request.GET['username']
	password = request.GET['password']
	user = authenticate(request, username=userName, password=password)
	if user is not None:
			login(request, user)
	if request.user.is_authenticated:	
		dataset = mongoform.allSessions(request.user.id)
		profile = mongoform.get_profile(request.user.id) 
		if (dataset == -1 or profile == 0):
			messages = "Database Error: Failed to retrive data from database."
			render = "home"
			context = {"Message": messages, "render": render}
			return JsonResponse(context)
		context = {"sessions" : dataset, "profile" : profile}
		pdf = render_to_pdf('symptomtracker/printReport.html', context)
		response = HttpResponse(pdf, content_type='application/pdf')
		filename = "Covid_Status_Report_of_%s.pdf" %(request.user.first_name)
		content = "attachment; filename=%s" %(filename)
		response['Content-Disposition'] = content
		return response
	messages = "Authentication Error."
	render = "tracker"
	context = {"Message": messages, "render": render}
	return JsonResponse(context)

#Symptom tracker api
@csrf_exempt
def tracker(request):
	userName = request.GET['username']
	password = request.GET['password']
	user = authenticate(request, username=userName, password=password)
	if user is not None:
			login(request, user)
			
	if request.user.is_authenticated:
		if (request.user.first_name == ""):
			messages = "Complete registration."
			render = "edit_profile"
			context = {"Message": messages, "render": render}
			return JsonResponse(context)
		#on post req for ending the current session
		if request.method == 'POST' and 'EndSession' in request.POST:
			timeNow = datetime.now().astimezone(pytz.timezone('Asia/Colombo'))
			date_now = timeNow.strftime('%d-%m-%Y')
			end_err = mongoform.endSession(request.user.id, date_now)
			if end_err != 0:
				messages.info(request, "Database Error: Couldn't access the database")
			else:
				messages = "Success"
			render = "tracker"
			context = {"Message": messages, "render": render}
			return JsonResponse(context)
		dataset = mongoform.allSessions(request.user.id)
		profile = mongoform.get_profile(request.user.id) 
		if (dataset == -1 or profile == 0):
			messages = "Database Error: Failed to retrive data from database."
			render = "home"
			context = {"Message": messages, "render": render}
			return JsonResponse(context)
		patient_data = '''Hello '''+request.user.first_name+'''!\n'''
		if(dataset == 0):
			patient_data +='''\nThere are no any ongoing or past sessions. Add daily symptoms to start a new session.'''
		else:
			if(dataset[-1]['Ending_date'] != ''):
				patient_data +='''\nThere are no any ongoing or past sessions. Add daily symptoms to start a new session.'''
			else:
				last_result = dataset[-1]['days'][-1]['Results'][10]
				if( last_result == '0'):
					patient_data +='''\nCongratulation! You don’t seem to have been affected by Covid-19. Please continue the session for few more days for better analysis. Stay safe!'''
				elif( last_result == '1'):
					patient_data +='''\nIt seems you may have been affected by Covid-19. It is likely to be the 1st or 2nd day of having the virus. Stay isolated and continue the session for better analysis. Drink hot water!'''
				elif( last_result == '3'):
					patient_data +='''\nIt seems you may have been affected by Covid-19. It is likely to be the 3rd day of having the virus. Stay isolated and continue the session for better analysis. Drink hot water!'''
				elif( last_result == '4'):
					patient_data +='''\nIt seems you may have been affected by Covid-19. It is likely to be the 4th day of having the virus. Get ready to do a PCR/Antigen test if the symptoms get worse.'''
				elif( last_result == '5'):
					patient_data +='''\nIt seems you may have been affected by Covid-19. It is likely to be the 5th day of having the virus. We highly recommend you to get a PCR/Antigen test as soon as possible.'''
				elif( last_result == '6'):
					patient_data +='''\nIt seems you may have been affected by Covid-19. It is likely to be the 6th day of having the virus. We highly recommend you to get a PCR/Antigen test as soon as possible. Be ready to get hospitalized if symptoms get worse.'''
				elif( last_result == '7'):
					patient_data +='''\nIt seems that you have been affected by Covid-19 for about 7 days. Please get hosptalized within the next couple of days for proper treatements.'''
				elif( last_result == '8'):
					patient_data +='''\nIt seems that you have been affected by Covid-19 for 8 or 9 days. Hospitalisation or medical supervision is needed for you to get recovered. There's chance of getting sepsis if proper treatments are not done.'''
				elif( last_result == '10'):
					patient_data +='''\nIt seems that you have been affected by Covid-19 for about 10 days. Hospitalisation or medical supervision is highly required for you to get recovered. There's chance of getting sepsis if proper treatments are not done. Your situation could be critical.'''
				elif( last_result == '11'):
					patient_data +='''\nYou seem to be in a critical situation. The analysis shows that you have been affected by covid for more than 11 days. You are adviced to get ICU treatments as soon as possible.'''
				patient_data +='''\n'''
				if(profile[9]!= '' or profile[10]!= '' or profile[11]!= '' or profile[12]!= '' or profile[13]!= ''):
					patient_data += '''\nYou have mentioned details of having,'''
					if(profile[9]!=''):
						patient_data += '''\nCardiovascular Disease'''
					if(profile[10]!=''):
						patient_data += '''\nDiabetes'''
					if(profile[11]!=''):
						patient_data += '''\nChronic Respiratory Disease'''
					if(profile[12]!=''):
						patient_data += '''\nCancer'''
					if(profile[13]!=''):
						patient_data += '''\nSpecial health conditions'''
					patient_data += '''\nPlease contact an specialist and get advice without a delay since coronavirus could be fatal to someone with aforementiond conditions.'''
		messages = "Success"
		render = "tracker"
		context = {"Message": messages, "render": render,"Sessions" : dataset, "Profile" : profile, "patient_msg": patient_data}
		return JsonResponse(context)
	messages = 'Please login to use the symptom tracker'
	render = "home"
	context = {"Message": messages, "render": render}
	return JsonResponse(context)

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

#Symptom insertion api
@csrf_exempt
def daily_session(request):
	userName = request.GET['username']
	password = request.GET['password']
	user = authenticate(request, username=userName, password=password)
	if user is not None:
			login(request, user)
			
	if request.user.is_authenticated:
		if (request.user.first_name == ""):
			messages = "Complete registration."
			render = "edit_profile"
			context = {"Message": messages, "render": render}
			return JsonResponse(context)
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
				messages = "Database Error: Couldn't save data to the database"
			else:
				messages = "Success"
			render = "tracker"
			context = {"Message": messages, "render": render}
			return JsonResponse(context)
		#Getting an array of days of the last session
		days_arr = mongoform.lastSession(request.user.id)
		if days_arr == -1:
			messages.info(request, "Database Error: Couldn't access the database. Please try again later.")
			render = "tracker"
			context = {"Message": messages, "render": render}
			return JsonResponse(context)
		elif days_arr == 0:
			messages = "Success"
			render = "daily_session"
			context = {"Message": messages, "render": render}
			return JsonResponse(context)
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
						messages = "You have to wait "+str(wait_time.hour)+" hours and "+str(wait_time.minute)+" minutes for the next session."
						render = "tracker"
						context = {"Message": messages, "render": render}
						return JsonResponse(context)
				messages = "Success"
				render = "daily_session"
				context = {"Message": messages, "render": render}
				return JsonResponse(context)
			messages = "You have completed two sessions for today! Please enter your symptoms again tomorrow."
			render = "tracker"
			context = {"Message": messages, "render": render}
			return JsonResponse(context)
	messages = 'Please login to use the symptom tracker'
	render = "home"
	context = {"Message": messages, "render": render}
	return JsonResponse(context)

#Admin panel api
@csrf_exempt
def admin_p(request):
	userName = request.GET['username']
	password = request.GET['password']
	user = authenticate(request, username=userName, password=password)
	if user is not None:
			login(request, user)
			
	if request.user.is_superuser:
		User = get_user_model()
		users = User.objects.all()
		messages = "Success"
		if request.method == 'POST': #to ensure the system will have at least 1 admin
			for thisuser in users:
				#Changing admin privilages
				if thisuser.username in request.POST:
					if thisuser.is_staff:
						if (request.user == thisuser):
							messages = "You can't remove your own privileges!"
						else:
							thisuser.is_staff = False
							thisuser.is_superuser = False
							messages = "Success"
							thisuser.save()
						break
					else:
						thisuser.is_staff = True
						messages = "Success"
						thisuser.save()
						break
				elif thisuser.username+"adm" in request.POST:
					if thisuser.is_superuser:
						if (request.user == thisuser):
							messages = "You can't remove your own privileges!"
						else:
							thisuser.is_superuser = False
							messages = "Success"
							thisuser.save()
						break
					else:
						thisuser.is_superuser = True
						thisuser.is_staff = True
						messages = "Success"
						thisuser.save()
						break
		newusers = User.objects.all()
		newusersarr = []
		for each in newusers:
			user_dict = {}
			user_dict["Username"] = each.username
			user_dict["Full_Name"] = each.get_full_name()
			user_dict["Email"] = each.email
			user_dict["Is_staff"] = each.is_staff
			user_dict["Is_admin"] = each.is_superuser
			newusersarr.append(user_dict)
		render = "adminpanel"
		context={"Message": messages, "render": render, 'users': newusersarr}
		return JsonResponse(context)
	messages = 'Access denied!'
	render = "home"
	context = {"Message": messages, "render": render}
	return JsonResponse(context)

#Staff panel api
@csrf_exempt
def staff_p(request):
	userName = request.GET['username']
	password = request.GET['password']
	user = authenticate(request, username=userName, password=password)
	if user is not None:
			login(request, user)
			
	if request.user.is_staff:
		#Sending contact and location data for staff panel
		cont = mongoform.getContacts()
		map_ = mongoform.getMap()
		if cont == 0 or map_ == 0:
			messages = "Database Error: Failed to get some data from database."
		else:
			messages = "Success"

		contArr = JSONEncoder().encode(cont)
		contArr = json.loads(contArr)
		mapArr = JSONEncoder().encode(map_)
		mapArr = json.loads(mapArr)

		#Updating contact data
		if request.method == 'POST' and 'update' in request.POST:
			data = request.POST.get('updateData')
			cont_data = json.loads(data, strict=False)
			if mongoform.addContacts(cont_data) == -1:
				messages = "Database Error: Failed to access the database."
			else:
				messages = "Success"
		#Updating location data
		if request.method == 'POST' and 'updateLoc' in request.POST:
			data = request.POST.get('updateDataLoc')
			loc_data = json.loads(data, strict=False)
			if mongoform.addLoc(loc_data) == -1:
				messages = "Database Error: Failed to access the database."
			else:
				messages = "Success"
		#Deleting contact data
		if request.method == 'POST' and 'delete' in request.POST:
			data = request.POST.get('deleteData')
			if mongoform.delContacts(data) == -1:
				messages = "Database Error: Failed to delete."
			else:
				messages = "Success"
		#Deleting location data
		if request.method == 'POST' and 'deleteLoc' in request.POST:
			data = request.POST.get('deleteDataLoc')
			if mongoform.delLoc(data) == -1:
				messages = "Database Error: Failed to delete."
			else:
				messages = "Success"

		render = "staffpanel"
		context = {"Message": messages, "render": render, "contacts": contArr, "locations":mapArr}
		return JsonResponse(context)
	messages = 'Access denied!'
	render = "home"
	context = {"Message": messages, "render": render}
	return JsonResponse(context)



#Get the map
#to access db
from decouple import config
from pymongo import MongoClient


client = MongoClient(config('DB_CONNECTION'))
database = client.get_database('CST') 

# Calling the MAP 
def map(request):
	mapArr = getMap()
	if mapArr == 0:
		messages = "Database Error: Failed to get data from database."
	else:
		messages = "Success"
	data = JSONEncoder().encode(mapArr)
	data = json.loads(data)
	map_con = config('MAP_CON') #Map connection string
	render = "map"
	context = { "Message": messages, "render": render, "map_connection": map_con, "locations": data}
	return JsonResponse(context)

#Getting Ma data from the database
def getMap():
	try:
		db = database.locations.find()
		arr = list(db)
		client.close()
		return arr
	except:
		client.close()
		return 0