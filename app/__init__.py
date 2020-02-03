from flask import Flask,request,jsonify,send_file,make_response
from flask_restful import Api,Resource,reqparse
from app.tensorflow_model import *
import base64
from io import StringIO,BytesIO
from skimage.io import imsave
app = Flask(__name__)
api = Api(app)

kmodel = getModel()


parser = reqparse.RequestParser()
parser.add_argument("image_b64")

@app.route('/')
@app.route('/index')
def index():
    return "Hello World"

class Generate(Resource):
    def get(self):
        predict(kmodel)
        return send_file('res.jpg',mimetype='image/jpg')
    def post(self):
        args = parser.parse_args()
        result = predict(kmodel,args["image_b64"])
        strIO = BytesIO()
        imsave(strIO,result,plugin='pil',format_str='png')
        strIO.seek(0)
        #return base64.b64encode(resultb64.tobytes()).decode('utf-8')
        #response = make_response(send_file(strIO,mimetype='image/png'))
        response = base64.b64encode(strIO.getvalue())
        print(response)
        return make_response(response)
        #return send_file(strIO,mimetype='image/png')

api.add_resource(Generate,'/gen')
app.run(host="0.0.0.0",port='5000')