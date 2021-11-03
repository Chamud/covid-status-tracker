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



#Home page
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

#Show profile page
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
		context = {"Message": messages, "render": render, "Account_data": acc_data, "user_data" : edit_data}
		return JsonResponse(context)
	messages = "Please login to access the profile"
	render = "home"
	context = {"Message": messages, "render": render}
	return JsonResponse(context)
	
#Registration page
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