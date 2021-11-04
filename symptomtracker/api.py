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
from django.middleware.csrf import get_token

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
		"Profile": "https://covidstatustracker.herokuapp.com/api/profile",
		"Edit_Profile": "https://covidstatustracker.herokuapp.com/api/edit_profile",
		"Register": "https://covidstatustracker.herokuapp.com/api/register",
		"Login": "https://covidstatustracker.herokuapp.com/api/login",
		"Logout": "https://covidstatustracker.herokuapp.com/api/logout",

	}
	return JsonResponse(context)

#Home api
def home(request):
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
	context = {"Message": messages, "render": render, "user": userfname, "media": url, "contacts": data }
	return JsonResponse(context)

#Show profile api
def profile(request):
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
def register(request):
	token = get_token(request)
	if request.method == 'POST': #post data : csrfmiddlewaretoken, username, email, password1, password2
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
		context = {"Message": messages, "render": render, 'form_token':token, "errors": form.errors.as_text()}
		return JsonResponse(context)
	messages = "Success"
	render = "register"
	context = {"Message": messages, "render": render, 'form_token':token}
	return JsonResponse(context)

#Login api
def loginuser(request):
	token = get_token(request)
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
		context = {"Message": messages, "render": render, 'form_token':token}
		return JsonResponse(context)
	messages = "Success"
	render = "login"
	context = {"Message": messages, "render": render, 'form_token':token}
	return JsonResponse(context)

#Logout api
def logoutuser(request):
	logout(request)
	messages = "Success"
	render = "home"
	context = {"Message": messages, "render": render}
	return JsonResponse(context)

#Edit profile page
def edit_profile(request):
	token = get_token(request)
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
			context = {"Message": messages, "render": render, 'form_token':token}
			return JsonResponse(context)
		edit_data = mongoform.get_profile(request.user.id) 
		if (edit_data == 0):
			messages = "Database Error: Failed to retrive data from database."
			render = "home"
			context = {"Message": messages, "render": render}
			return JsonResponse(context)
		messages = "Success"
		render = "edit_profile"
		context = { "Message": messages, "render": render, 'form_token':token, 'profile_data' : edit_data}
		return JsonResponse(context)
	messages = "Login to access"
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