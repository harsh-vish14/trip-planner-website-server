import firebase_admin
from firebase_admin import credentials, firestore
from flask import Flask, request, jsonify
app = Flask(__name__)
FlightData = [
    {
        "name": 'IndiGo.',
        'description': 'Lorem ipsum dolor sit amet consectetur adipisicing elit. Maxime mollitia,\
molestiae quas vel sint commodi repudiandae consequuntur voluptatum laborum\
numquam blanditiis harum quisquam eius sed odit fugiat iusto fuga praesentium\
optio, eaque rerum! Provident similique accusantium nemo autem',
        'image': 'https://cdn.dnaindia.com/sites/default/files/styles/full/public/2018/08/26/722825-indigo.jpg',
        'price': 10000,
        'year':2021,
        'month': 3,
        'day':11
    },
    {
        'name':'Air India',
        'description':'Reprehenderit,\
quia. Quo neque error repudiandae fuga? Ipsa laudantium molestias eos\
sapiente officiis modi at sunt excepturi expedita sint? Sed quibusdam\
recusandae alias error harum maxime adipisci amet laborum.',
        'image':'https://akm-img-a-in.tosshub.com/indiatoday/images/story/202004/AIR_INDIA_PTI_0.jpeg?Fyhus6fwqLtTT__xPTZxPdqwvUaMMx5o&size=770:433',
        'price':12000,
        'year':2021,
        'month': 4,
        'day':10
    },
    {
        'name':'SpiceJet',
        'description':'Perspiciatis\
minima nesciunt dolorem! Officiis iure rerum voluptates a cumque velit\
quibusdam sed amet tempora. Sit laborum ab, eius fugit doloribus tenetur \
fugiat, temporibus enim commodi iusto libero magni deleniti quod quam \
consequuntur! Commodi minima excepturi repudiandae velit hic maxime\
doloremque',
        'image':'https://i.gadgets360cdn.com/large/spicejet_facebook_1580399464034.jpg',
        'price':13999,
        'year':2021,
        'month': 4,
        'day':20
    },
    {
        'name': 'GoAir',
        'description':'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Quisque nisl eros, \
pulvinar facilisis justo mollis, auctor consequat urna. Morbi a bibendum metus. \
Donec scelerisque sollicitudin enim eu venenatis.',
        'image': 'https://gumlet.assettype.com/freepressjournal%2F2020-09%2Fbcc3b7c1-ad63-43b4-aecd-26cdc62a0ec9%2FGoAir.jpg?w=1200',
        'price': 12999,
        'year': 2021,
        'month':4,
        'day':20
    },
    {
        'name': 'AirAsia India',
        'description': 'Lorem ipsum dolor sit amet consectetur adipisicing elit. Maxime mollitia,\
molestiae quas vel sint commodi repudiandae consequuntur voluptatum laborum\
numquam blanditiis harum quisquam eius sed odit fugiat iusto fuga praesentium\
optio, eaque rerum! Provident similique accusantium nemo autem.',
        'image':'https://img.theweek.in/content/dam/week/news/biz-tech/images/2020/6/16/air-asia-file-salil.jpg',
        'price': 10999,
        'year':2021,
        'month':4,
        'day':21
    },
    {
        'name':'Vistara',
        'description':'Veritatis\
obcaecati tenetur iure eius earum ut molestias architecto voluptate aliquam\
nihil, eveniet aliquid culpa officia aut! Impedit sit sunt quaerat, odit,\
tenetur error, harum nesciunt ipsum debitis quas aliquid.',
        'image':'https://static.theprint.in/wp-content/uploads/2019/08/Vistara-Airlines.jpg',
        'price':9000,
        'year':2021,
        'month':4,
        'day':22
    },
    {
        'name':'TruJet',
        'description':'Lorem ipsum dolor sit amet consectetur adipisicing elit. Maxime mollitia,\
molestiae quas vel sint commodi repudiandae consequuntur voluptatum laborum\
numquam blanditiis harum quisquam eius sed odit fugiat iusto fuga praesentium\
optio, eaque rerum! Provident similique accusantium nemo autem.',
        'price':9999,
        'year':2021,
        'month':4,
        'day':19
    }
]
cred = credentials.Certificate("./key.json")
firebase_admin.initialize_app(cred)
db = firestore.client()
ref = db.collection('users')


@app.route('/', methods=['GET'])
def home():
    return jsonify({
        'message': "hello from flask server"
    })


@app.route('/userLogin', methods=['POST'])
def sendData():
    userData = request.json
    print(userData[0])
    db.collection('flight').document('flights').set(
        {
            "flightData" : userData
        }
    )
    # ref.document(userData['uid']).set({})
    return jsonify({
        'status': 200,
        'message': 'done'
    })


@app.route('/flightQuery/<money>/<year>/<month>/<day>', methods=['GET'])
def fight(money = 0,year = 0,month = 0,day = 0):
    print(FlightData)

    # filterData = []
    # print(money,year,month,day)
    # for i in FlightData:
    #     if int(money) >= i['price'] and int(year) >= i['year'] and int(month) >= i['month'] and int(day) >= i['day']:
    #         filterData.append(i)

    return jsonify({
        'message':'done'
    })

# @app.route('/')
# def notFount():
    # return jsonify({
        # 'status':404,
        # 'message':'invalid api call'
    # })

if (__name__ == "__main__"):
    app.run(debug=True)