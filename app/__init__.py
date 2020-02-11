from flask import Flask,request,jsonify,send_file,make_response
from flask_restful import Api,Resource,reqparse
from flask_cors import CORS
from app.tensorflow_model import *
import base64
from io import StringIO,BytesIO
from skimage.io import imsave
app = Flask(__name__)
CORS(app)
api = Api(app)

modelname = "pix2pix_lambda5"
modelList = getModels()
kmodel = getModel(modelname)


parser = reqparse.RequestParser()
parser.add_argument("image_b64")

@app.route('/')
@app.route('/index')
def index():
    return "Hello World"

class ListModels(Resource):
    def get(self):
        return make_response(jsonify(getModels()))

class Model(Resource):
    def get(self):
        global modelname
        return make_response(modelname)
    def post(self,model):
        global modelname
        global kmodel
        if model in modelList:
            try:
                kmodel = getModel(model)
                modelname = model
                return {"model":model},200
            except Exception:
                return {"Model empty"},404
        else:
            return {"Model not existent"},400


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
        #print(response)
        return make_response(response)
        #return send_file(strIO,mimetype='image/png')

api.add_resource(Generate,'/gen')
api.add_resource(ListModels,'/list')
api.add_resource(Model,'/model','/model/<model>')
app.run(host="0.0.0.0",port='5050')
