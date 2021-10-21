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

def edit_user(id, dataset):
	try:
		db_id = "{\"ID\": \""+str(id)+"\"}"
		db_record = "{ \"$set\":{ \"Name.First\": \""+dataset[0]+"\", \"Name.Last\": \""+dataset[1]+"\", \"ID_.number\": \""+dataset[2]+"\", \"ID_.type\": \""+dataset[3]+"\", \"Address\": \""+dataset[4]+"\", \"Date_of_Birth\": \""+dataset[5]+"\", \"Contact_Number\": \""+dataset[6]+"\",  \"Vaccinated?\": \""+dataset[7]+"\", \"Affected_by_Covid?\": \""+dataset[8]+"\", \"Health_Conditions.Cardiovascular_Disease\": \""+dataset[9]+"\", \"Health_Conditions.Diabetes\": \""+dataset[10]+"\", \"Health_Conditions.Chronic_Respiratory_Disease\": \""+dataset[11]+"\", \"Health_Conditions.Cancer\": \""+dataset[12]+"\", \"Health_Conditions.Other\": \""+dataset[13]+"\"}}"
		db_obj1 = json.loads(db_id, strict=False)
		db_obj2 = json.loads(db_record, strict=False)
		database.UserData.update(db_obj1, db_obj2)
		client.close()
		return 0
	except:
		client.close()
		return 1

def get_profile(id):
	try:
		db_record = "{\"ID\": \""+str(id)+"\" }"
		db_obj = json.loads(db_record, strict=False)
		profile = database.UserData.find_one(db_obj)
		profileData = []
		profileData.append(profile['Name']['First'])										#0
		profileData.append(profile['Name']['Last'])											#1
		profileData.append(profile['ID_']['number'])										#2
		profileData.append(profile['ID_']['type'])											#3
		profileData.append(profile['Address'])												#4
		profileData.append(profile['Date_of_Birth'])										#5
		profileData.append(profile['Contact_Number'])										#6
		profileData.append(profile['Vaccinated?'])											#7
		profileData.append(profile['Affected_by_Covid?'])									#8
		profileData.append(profile['Health_Conditions']['Cardiovascular_Disease'])			#9	
		profileData.append(profile['Health_Conditions']['Diabetes'])						#10	
		profileData.append(profile['Health_Conditions']['Chronic_Respiratory_Disease'])		#11
		profileData.append(profile['Health_Conditions']['Cancer'])							#12
		profileData.append(profile['Health_Conditions']['Other'])							#13			
		client.close()
		return profileData
	except:
		client.close()
		return 0

def saveSymptoms(input_data, results):
	try:
		db_ID = "{\"ID\": \""+str(input_data[0])+"\" }"
		db_obj = json.loads(db_ID, strict=False)
		profile = database.UserData.find_one(db_obj)
		
		data_arrays = "\"Input_Data\" : [\""+input_data[1]+"\", \""+input_data[2]+"\", "+str(input_data[3])+", "+str(input_data[4])+", "+str(input_data[5])+", "+str(input_data[6])+", "+str(input_data[7])+", "+str(input_data[8])+", "+str(input_data[9])+", "+str(input_data[10])+", "+str(input_data[11])+", "+str(input_data[12])+", "+str(input_data[13])+", "+str(input_data[14])+", "+str(input_data[15])+"], \"Results\" : ["+str(results[0])+", "+str(results[1])+", "+str(results[2])+", "+str(results[3])+", "+str(results[4])+", "+str(results[5])+", "+str(results[6])+", "+str(results[7])+", "+str(results[8])+", "+str(results[9])+", \""+results[10]+"\", \""+results[11]+"\"] "

		if 'Sessions' in profile:
			session = profile['Sessions']
			if session[-1]['Ending_date'] == "":
				Session_num = session[-1]['Session_Number']
				db_id = "{ \"ID\": \""+str(input_data[0])+"\", \"Sessions.Session_Number\": \""+str(Session_num)+"\"  }"
				db_record = "{ \"$push\": { \"Sessions.$.days\": {"+data_arrays+"} } }"
				db_obj1 = json.loads(db_id, strict=False)
				db_obj2 = json.loads(db_record, strict=False)
				database.UserData.update(db_obj1,db_obj2)
			else:
				Session_num = int(session[-1]['Session_Number']) + 1
				db_id = "{ \"ID\": \""+str(input_data[0])+"\" }"																											
				db_record = "{ \"$push\": { \"Sessions\": {\"Session_Number\" :\""+str(Session_num)+"\", \"Starting_Date\" : \""+input_data[1]+"\", \"Ending_date\": \"\", \"days\":[{"+data_arrays+" } ] } } }"
				db_obj1 = json.loads(db_id, strict=False)
				db_obj2 = json.loads(db_record, strict=False)
				database.UserData.update(db_obj1,db_obj2)
		else:
			db_id = "{ \"ID\": \""+str(input_data[0])+"\" }"																											
			db_record = "{ \"$push\": { \"Sessions\": {\"Session_Number\" :\"1\", \"Starting_Date\" : \""+input_data[1]+"\", \"Ending_date\": \"\", \"days\":[{"+data_arrays+" } ] } } }"
			db_obj1 = json.loads(db_id, strict=False)
			db_obj2 = json.loads(db_record, strict=False)
			database.UserData.update(db_obj1,db_obj2)
		client.close()
		return 0
	except:
		client.close()
		return -1
	

def lastSession(id):
	try:
		db_ID = "{\"ID\": \""+str(id)+"\" }"
		db_obj = json.loads(db_ID, strict=False)
		profile = database.UserData.find_one(db_obj)

		if 'Sessions' in profile:
				if profile['Sessions'][-1]['Ending_date'] == "":
					client.close()
					return profile['Sessions'][-1]['days']
		client.close()
		return 0
	except:
		client.close()
		return -1

def allSessions(id):
	try:
		db_ID = "{\"ID\": \""+str(id)+"\" }"
		db_obj = json.loads(db_ID, strict=False)
		profile = database.UserData.find_one(db_obj)
		if 'Sessions' in profile:
			client.close()
			return profile['Sessions']
		client.close()
		return 0
	except:
		client.close()
		return -1


def endSession(id, date):
	db_ID = "{\"ID\": \""+str(id)+"\" }"
	db_obj = json.loads(db_ID, strict=False)
	profile = database.UserData.find_one(db_obj)
	if 'Sessions' in profile:
		session = profile['Sessions']
		if session[-1]['Ending_date'] == "":
			Session_num = session[-1]['Session_Number']
			db_id = "{ \"ID\": \""+str(id)+"\", \"Sessions.Session_Number\": \""+str(Session_num)+"\"  }"
			db_record = "{ \"$set\":{ \"Sessions.$.Ending_date\" : \""+date+"\" } }"
			db_obj1 = json.loads(db_id, strict=False)
			db_obj2 = json.loads(db_record, strict=False)
			database.UserData.update(db_obj1, db_obj2)
	client.close()
	return 0