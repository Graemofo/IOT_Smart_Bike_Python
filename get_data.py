from firebase import firebase
firebase = firebase.FirebaseApplication('https://iot-bike-4e692.firebaseio.com/')
result = firebase.get('/Resistance', None)
print (result)
