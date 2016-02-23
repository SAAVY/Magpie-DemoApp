import json

from flask import flash
from flask import Flask
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from flask_bootstrap import Bootstrap
from flask_wtf import Form
from flask_wtf.csrf import CsrfProtect
from wtforms import SubmitField
from wtforms import TextField
from wtforms.validators import ValidationError
import requests

import config
from constants import StatusCode


api_url = config.PROD_API_URL

if config.IS_DEV:
    api_url = config.DEV_API_URL


class MetadataRequestForm(Form):

    def is_valid_url(form, field):
        if field.data == "":
            error_msg = 'Must not be empty field'
            flash("URL Field Error: " + error_msg, 'error')
            raise ValidationError(error_msg)

    text_field = TextField('Website URL:', [is_valid_url], description='Enter in a website url to extract, eg: http://www.youtube.com/watch?v=dQw4w9WgXcQ')
    submit_button = SubmitField('Create Metadata')


def create_app(configfile=None):
    app = Flask(__name__)
    Bootstrap(app)
    app.config['SECRET_KEY'] = 'devkey'
    csrf = CsrfProtect()
    csrf.init_app(app)

    def get_response(url):
        args = {'src': url}
        response = requests.get(api_url, params=args)
        return response.json()

    def make_pretty_json(response_json):
        json_output = json.dumps(response_json, indent=4, separators=(',', ': '))
        return json_output

    def show_response_errors(response_json):
        if (response_json['status'] != StatusCode.OK and response_json['error_message']):
            flash("ERROR %d: %s" % (response_json['status'], response_json['error_message']), 'error')
            return True
        return False

    @app.route('/', methods=('GET', 'POST'))
    def index():
        src_url = None
        json_output = None
        json = None

        if request.args.get('src'):
            src_url = request.args.get('src')

        form = MetadataRequestForm()

        if form.validate_on_submit():  # to get error messages to the browser
            src_url = form.text_field.data
            return redirect(url_for('index', src=src_url))

        if src_url:
            json = get_response(src_url)
            json_output = make_pretty_json(json)
            display_url = json['data']['url']
            if not show_response_errors(json):
                return render_template('base.html', form=form, json_output=json_output, json=json, display_url=display_url)

        return render_template('base.html', form=form)

    return app

if __name__ == '__main__':
    create_app().run(debug=config.IS_DEV, port=config.PORT_NUMBER)
