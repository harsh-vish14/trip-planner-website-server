import firebase_admin
from firebase_admin import credentials, firestore
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

cred = credentials.Certificate("./key.json")
firebase_admin.initialize_app(cred)
db = firestore.client()
ref = db.collection('users')


@app.route('/', methods=['GET'])
def home():
    return jsonify({
        'message': "hello from flask server"
    })

@app.route('/hotels',methods=['GET'])
def hotel():
    return jsonify({
        'hotels':[]
    })

@app.route('/hotels/<add>',methods=['GET'])
def hotelsFillter(add = ''):
    hotels = db.collection('hotel').document('hotels').get().to_dic()
    filteredHotel = []
    for hotel in hotels:
        if hotel.Localtion == add:
            filteredHotel.append(hotel)
    return filteredHotel



@app.route('/userLogin', methods=['POST'])
def sendData():
    userData = request.json
    print(userData[0])
    # db.collection('hotel').document('hotels').set(
    #     {
    #         "hotelsData": userData,
    #     }
    # )
    doc_ref = db.collection('users').document(userData['uid'])
    doc = doc_ref.get()
    if doc.exists:
        doc_ref.set({});
    else:
        doc_ref.set({
            'name':userData['name'],
            'email':userData['email'],
            'userPhoto': userData['userPhoto']
        },);
    return jsonify({
        'status': 200,
        'message': 'done'
    })


@app.route('/flightQuery/<money>/<year>/<month>/<day>', methods=['GET'])
def fight(money=0, year=0, month=0, day=0):
    doc = dict(db.collection('flight').document('flights').get().to_dict())
    filterData = []
    print(money, year, month, day)
    for i in doc['flightData']:
        if int(money) >= i['price'] and int(year) >= i['year'] and int(month) >= i['month']:
            filterData.append(i)
    return jsonify(filterData)


# @app.route('/')
# def notFount():
# return jsonify({
# 'status':404,
# 'message':'invalid api call'
# })

if (__name__ == "__main__"):
    app.run(debug=True)
