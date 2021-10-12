from decouple import config
from pymongo import MongoClient
import json

client = MongoClient(config('DB_CONNECTION'))
database = client.get_database('CST') 


def pre_reg_new_user(user):
	try:
		db_record = "{\"ID\": \""+str(user.id)+"\", \"Username\": \""+user.username+"\", \"Email\": \""+user.email+"\" }"
		db_obj = json.loads(db_record, strict=False)
		database.UserData.insert_one(db_obj)
		client.close()
		return 0
	except:
		client.close()
		return 1

def reg_new_user(id, dataset):
	try:
		IDtype = dataset[3]
		vaccinated = dataset[7]
		db_id = "{\"ID\": \""+str(id)+"\"}"
		db_record = "{ \"$set\":{ \"First_Name\": \""+dataset[0]+"\", \"Last_Name\": \""+dataset[1]+"\", \"ID_number\": \""+dataset[2]+"\", \"ID_type\": \""+dataset[3]+"\", \"Address\": \""+dataset[4]+"\", \"Date_of_Birth\": \""+dataset[5]+"\", \"Contact_Number\": \""+dataset[6]+"\",  \"Vaccinated?\": \""+dataset[7]+"\", \"Affected_by_Covid?\": \""+dataset[8]+"\", \"Health_Conditions.Cardiovascular_Disease\": \""+dataset[9]+"\", \"Health_Conditions.Diabetes\": \""+dataset[10]+"\", \"Health_Conditions.Chronic_Respiratory_Disease\": \""+dataset[11]+"\", \"Health_Conditions.Cancer\": \""+dataset[12]+"\", \"Health_Conditions.Other\": \""+dataset[13]+"\"}}"
		db_obj1 = json.loads(db_id, strict=False)
		db_obj2 = json.loads(db_record, strict=False)
		database.UserData.update(db_obj1, db_obj2)
		client.close()
		return 0
	except:
		client.close()
		return 1