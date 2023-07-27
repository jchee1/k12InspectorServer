from flask import Flask, request, json, Response, make_response
from pymongo import MongoClient
from bson.json_util import dumps
from flask_cors import CORS

app = Flask(__name__, template_folder='./templates')
#application = Flask(__name__, template_folder='./templates')
#app = application
CORS(app)

def make_cors_response(*args):
    response = make_response(*args)
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Credentials', 'true')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
    response.headers.add('Access-Control-Allow-Headers', 'Cache-Control')
    response.headers.add('Access-Control-Allow-Headers', 'X-Requested-With')
    response.headers.add('Access-Control-Allow-Headers', 'Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
    return response

uri = "mongodb://localhost:27017"
client = MongoClient(uri)
db = client['testdb']
collection = db['test_column']

#    @Override
#    public void doFilter(ServletRequest req, ServletResponse res, FilterChain chain) throws IOException, ServletException {
#        final HttpServletResponse response = (HttpServletResponse) res;
#        response.setHeader("Access-Control-Allow-Origin", "*");
#        response.setHeader("Access-Control-Allow-Methods", "POST, PUT, GET, OPTIONS, DELETE");
#        response.setHeader("Access-Control-Allow-Headers", "Authorization, Content-Type");
#        response.setHeader("Access-Control-Max-Age", "3600");
#        if ("OPTIONS".equalsIgnoreCase(((HttpServletRequest) req).getMethod())) {
#            response.setStatus(HttpServletResponse.SC_OK);
#        } else {
#            chain.doFilter(req, res);
#        }
#    }

@app.route('/')
def index():
    print("here")
    return "<h1 style='color:blue'>Hello There!</h1>"
    #return render_template('index.html')

@app.route('/save', methods=['POST', 'OPTIONS'])
def mongo_write():
    #print(request)
    if request.method == 'OPTIONS':
        print("options")
        return make_cors_response()
    print("got data")
    data = request.get_json()
    if data is None or data == {}:
        print("no data")
    print("before count")
    print(data)
    count = collection.count_documents({
        '$and': [
            {'report.school_district': {'$exists': True}},
            {'report.user_id': {'$exists': True}},
            {'report.grade': {'$exists': True}},
            {'report.request_method': data["report"]["request_method"]},
            {'report.leak_url': data["report"]["leak_url"]},
            {'report.initiator_domain': data["report"]["initiator_domain"]},
            {'report.url_leak_type': data["report"]["url_leak_type"]},
            {'report.body_leak_type': data["report"]["body_leak_type"]},
            {'report.tracker_info': data["report"]["tracker_info"]}
            ]
            })

    print(count)
    if count > 0:
        pass
    else:
        collection.insert_one(data)

    response = make_cors_response()
    return response

@app.route('/all', methods=['GET'])
def get_all():
    print("getting all from db")
    all_records = list(collection.find())
    print(all_records)
    return Response(response=dumps(all_records),
                    status=200,
                    mimetype='application/json')

# inserting simplest way to run flask over https
#if __name__ == "__main__":
#    app.run()
    #app.run(ssl_context=('cert.pem', 'key.pem'), debug=True)
