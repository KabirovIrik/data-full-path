from flask import Flask, render_template, request
import pandas as pd

from utils import *
from getResponse import *


#query_input = 'керамзитобетонные блоки в Уфе'
#url = 'https://ufa.promportal.su/tags/8433/bloki-keramzitobetonnie/'

app = Flask(__name__)

@app.route('/', methods=["POST", "GET"])
def index():
    if request.method == 'POST':
        form_res = request.form.to_dict()
        result = getResponse(form_res['query'], form_res['URL'])
        result['query'] = form_res['query']
        result['URL'] = form_res['URL']
        return render_template('result.html', quries_ufa=quries_ufa, result=result)
    return render_template('index.html', quries_ufa=quries_ufa)

if __name__ == "__main__":
    app.run()