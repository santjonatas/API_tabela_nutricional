from flask import Flask, render_template
from flask_wtf import FlaskForm
from flask_wtf.csrf import CSRFProtect
from pprint import pprint
import traceback
import json

from form.tabela_nutricional_form import TabelaNutricionalForm
from service.cohere_ia_service import CohereIaService

import os
from dotenv import load_dotenv


load_dotenv()


app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
csrf = CSRFProtect(app)

cohere_ia_service = CohereIaService() 

@app.route('/', methods=['GET', 'POST'])
def home():
    form: FlaskForm = TabelaNutricionalForm()

    info_alimento = None

    if form.validate_on_submit():
        try:
            pprint(form.to_dict())
            alimento = form.to_dict()

            produto = alimento.get('alimento')
            info_alimento = cohere_ia_service.obter_info_alimento(produto=produto)

            if info_alimento != '"O parâmetro informado não é um alimento."':
                info_alimento = json.loads(info_alimento)  

            return render_template('index.html', form=form, info_alimento=info_alimento)
        except Exception as e:
            stacktrace = traceback.format_exc()

    return render_template('index.html', form=form, info_alimento=info_alimento)

if __name__ == '__main__':
    app.run(debug=True)
