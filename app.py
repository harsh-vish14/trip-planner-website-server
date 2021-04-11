import firebase_admin
from firebase_admin import credentials, firestore
from flask import Flask, request, jsonify,redirect
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

@app.route(f'/updateUserFields/{Authkey}/remove',methods=['POST'])
@cross_origin()
def updateDetails():
    Data = request.get_json(force=True);
    doc_ref = db.collection('users').document(Data['uid'])
    doc = doc_ref.get()
    if doc.exists:
        doc_ref.update({Data['fieldName'] : firestore.ArrayRemove([Data['id']])})
    else:
        return jsonify({
            "Message":"Invalid user id"
        });    
    print(Data);
    return jsonify({
        "Message":"Data Updated successfully",
        'status': 200
    });

@app.route(f'/add-hotel/{Authkey}/<dbname>',methods=['POST'])
@cross_origin()
def hotelsAdd(dbname):
    Databases = ['hotel','flight','package']
    DataArrays = request.get_json(force=True);
    if(dbname in Databases):
        print(DataArrays)
        for data in DataArrays:
            db.collection(dbname).document(dbname+'s').update({dbname+"sData": firestore.ArrayUnion([data])})
            # print(data);
    else:
        return jsonify({
            "error":'invalid api call',
            "status": 400
        })
    # for hotel in hotelsArray:
    return jsonify({
        'message': 'Data added',
        'status':200
    })


@app.route('/hotels',methods=['GET'])
def hotelsFillter():
    hotels = db.collection('hotel').document('hotels').get().to_dict()
    hotels = hotels['hotelsData']
    return jsonify(hotels)

@app.route('/flightQuery/<money>/<year>/<month>/<day>', methods=['GET'])
def fight(money=0, year=0, month=0, day=0):
    doc = dict(db.collection('flight').document('flights').get().to_dict())
    filterData = []
    for i in doc['flightsData']:
        if int(money) >= i['price'] and int(year) >= i['year'] and int(month) >= i['month']:
            filterData.append(i)
    return jsonify(filterData)


@app.route('/userLogin', methods=['POST'])
@cross_origin()
def sendData():
    userData = request.get_json(force=True)
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

@app.route('/packages',methods=['GET'])
def packages():
    doc = dict(db.collection('package').document('packages').get().to_dict())
    doc = doc['packagesData']
    return jsonify(doc)

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

@app.route(f'/user/{Authkey}/<id>', methods=['GET'])
def user(id = 0):
    if(id != 0):
        # return jsonify({"id": id})
        doc_ref = db.collection('users').document(id)
        doc = doc_ref.get()
        amount = 0
        if doc.exists:
            updatedData = {
                'name': doc.to_dict()['name'],
                'email': doc.to_dict()['email'],
                'userPhoto': doc.to_dict()['userPhoto'],
                'flights': [],
                'hotels': [],
                'packages': [],
            }
            packageDoc = db.collection('package').document('packages').get().to_dict()
            hotelDoc = db.collection('hotel').document('hotels').get().to_dict()
            flightDoc = db.collection('flight').document('flights').get().to_dict()

            for flight in doc.to_dict()['flights']:
                for dbflight in flightDoc['flightsData']:
                    if (dbflight['id'] == flight):
                        updatedData['flights'].append(dbflight)
                        amount = amount + int(dbflight['price'])

            for hotel in doc.to_dict()['hotels']:
                for dbhotels in hotelDoc['hotelsData']:
                    if ( dbhotels['id'] == hotel):
                        updatedData['hotels'].append(dbhotels)
                        amount = amount + int(dbhotels['price'])

            for package in doc.to_dict()['packages']:
                for dbpackages in packageDoc['packagesData']:
                    if (dbpackages['id'] == package):
                        updatedData['packages'].append(dbpackages)
                        amount = amount + int(dbpackages['price'])

            return jsonify({
                "amount":amount,
                "Data":updatedData
            })
    return redirect("/Not-Found", code=302)


@app.route('/paymentDone', methods=['POST'])
@cross_origin()
def paymentDone():
    tokenData = request.get_json(force=True)
    doc_ref = db.collection('users').document(tokenData['uid'])
    doc = doc_ref.get()
    if doc.exists:
        doc_ref.update({
            "flights": [],
            "packages": [],
            "hotels": []
        })
    return jsonify({
        "message": "Payment is done successfully"
    })


@app.errorhandler(404)
def not_found(e):
    return jsonify({
        "err": 'invalid api call',
        "status":400,
    })

if (__name__ == "__main__"):
    app.run(debug=True)
