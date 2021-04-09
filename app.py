import firebase_admin
from firebase_admin import credentials, firestore
from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
import uuid

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
Authkey = '409bb257-c328-42bf-afe8-205f07a4f2be'

cred = credentials.Certificate("./key.json")
firebase_admin.initialize_app(cred)
db = firestore.client()
ref = db.collection('users')


@app.route('/', methods=['GET'])
def home():
    return jsonify({
        'message': uuid.uuid4()
    })

# @app.route('/hotels', methods=['GET'])
# def hotel():
#     return jsonify({
#         'hotels':'ikasd'
#     })

@app.route(f'/add-hotel/{Authkey}',methods=['POST'])
@cross_origin()
def hotelsAdd():
    hotelsArray = request.get_json(force=True);
    # for hotel in hotelsArray:


@app.route('/hotels',methods=['GET'])
def hotelsFillter():
    hotels = db.collection('hotel').document('hotels').get().to_dict()
    hotels = hotels['hotelsData']
    return jsonify(hotels)



@app.route('/userLogin', methods=['POST'])
@cross_origin()
def sendData():
    userData = request.get_json(force=True)
    # db.collection('hotel').document('hotels').set(
    #     {
    #         "hotelsData": userData,
    #     }
    # )
    doc_ref = db.collection('users').document(userData['uid'])

    doc = doc_ref.get()
    if doc.exists == False:
        doc_ref.set({
            'name':userData['name'],
            'email':userData['email'],
            'userPhoto': userData['userPhoto'],
            'flights': [],
            'packages': [],
            'hotels': []
        });
    return jsonify({
        "message": 'User added successfully',
        "status":200
    })

@app.route('/addFlight', methods=['POST'])
@cross_origin()
def add_flight():
    flightData = request.get_json(force=True)
    doc_ref = db.collection('users').document(flightData['uid'])
    # {u'regions': firestore.ArrayUnion([u'greater_virginia'])}
    doc_ref.update({u'flights': firestore.ArrayUnion([flightData['flightId']])})
    print(flightData)
    return jsonify({
        "message": 'User flight successfully',
        "status":200
    })


@app.route('/addHotels', methods=['POST'])
@cross_origin()
def add_hotels():
    hotelData = request.get_json(force=True)
    doc_ref = db.collection('users').document(hotelData['uid'])
    # {u'regions': firestore.ArrayUnion([u'greater_virginia'])}
    doc_ref.update({u'hotels': firestore.ArrayUnion([hotelData['hotelId']])})
    print(hotelData)
    return jsonify({
        "message": 'User flight successfully',
        "status":200
    })


@app.route('/addPackage', methods=['POST'])
@cross_origin()
def add_package():
    packageData = request.get_json(force=True)
    doc_ref = db.collection('users').document(packageData['uid'])
    # {u'regions': firestore.ArrayUnion([u'greater_virginia'])}
    doc_ref.update({u'packages': firestore.ArrayUnion([packageData['packageId']])})
    print(packageData)
    return jsonify({
        "message": 'User flight successfully',
        "status":200
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
@app.errorhandler(404)
def not_found(e):
    return jsonify({
        "err": 'invalid api call',
        "status":400,
    })

if (__name__ == "__main__"):
    app.run(debug=True)
