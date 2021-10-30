from django.shortcuts import render
from decouple import config

#to access db
from decouple import config
from pymongo import MongoClient


client = MongoClient(config('DB_CONNECTION'))
database = client.get_database('CST') 

# Create your views here.
def map(request):

	mapArr = getMap()
	if mapArr == 0:
		messages.info(request, "Database Error: Failed to get some data from database.")
	map_con = config('MAP_CON')

	context = { "locate": mapArr, "map_con": map_con}
	return render(request, 'map/map.html', context)

def getMap():
	try:
		db = database.locations.find()
		arr = list(db)
		client.close()
		return arr
	except:
		client.close()
		return 0