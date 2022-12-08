from flask import Flask, request, json, Response
from pymongo import MongoClient

app = Flask(__name__)

#print("testing mongo")

uri = "mongodb+srv://extensiondata.z0i6bq9.mongodb.net/?authSource=%24external&authMechanism=MONGODB-X509&retryWrites=true&w=majority"
client = MongoClient(uri,
                     tls=True,
                     tlsCertificateKeyFile='/root/edtech/X509-cert-1555286125965723181.pem')

db = client['edtechExtensionData']

collection = db['collectionData']
#mydict = { "name": "John", "address": "Highway 37" }
#x = collection.insert_one(mydict)
#print(client.list_database_names())


@app.route('/')
def index():
    return '<h1>index</h1>'

@app.route('/save', methods=['POST'])
def mongo_write():
    print("got data")
    data = request.get_json()
    if data is None or data == {}:
        print("no data")

    print(data)
    collection.insert_one(data)
    return Response(response=data,
                    status=200,
                    mimetype='application/json')
    