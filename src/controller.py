from flask import Blueprint, render_template

blueprint = Blueprint("module_a", __name__)


@blueprint.route('/', methods=['POST', 'GET'])
def index():
    return render_template('index.html')
