print('____________________________________________________________________________________________');
import requests

pload = {'username':'admin1','password':'5CPiu@gv5XYFSjU'}
q = 'https://covidstatustracker.herokuapp.com/api/profile'
p = 'http://127.0.0.1:8000/api/login'
r = requests.get(q, data=pload)
print(r.text)
