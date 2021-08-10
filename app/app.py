from flask import Flask, render_template, request, jsonify
from flask_restful import Resource, Api, reqparse
from urllib.parse import unquote

from utils import *
from convertInput import *

app = Flask(__name__)
api = Api(app)


# url

@app.route('/', methods=["POST", "GET"])
def index():
    if request.method == 'POST':
        form_res = request.form.to_dict()
        result = getResponse(form_res['query'], form_res['URL'])
        result['query'] = form_res['query']
        result['URL'] = form_res['URL']
        return render_template('result.html', quries_ufa=quries_ufa, result=result)
    return render_template('index.html', quries_ufa=quries_ufa)


# API

parser = reqparse.RequestParser()
parser.add_argument('url_page', type=str)
parser.add_argument('quiery_id', type=int)

class getQuerieslist(Resource):
    def get(self):
        return {'query_list':quries_ufa}

api.add_resource(getQuerieslist, '/get-list')


class analysPage(Resource):
    def get(self):
        args = parser.parse_args()
        url_page = unquote(args['url_page'])
        quiery_id = quries_ufa[args['quiery_id']]
        result = getResponse(quiery_id, url_page, is_api=True)
        print(result)
        return result

api.add_resource(analysPage, '/analys-page')


if __name__ == "__main__":
    app.run(debug=True)
    # curl http://127.0.0.1:5000/analys-page?quiery_id=123&url_page=https%3A%2F%2Fzzbeton.ru%2F
