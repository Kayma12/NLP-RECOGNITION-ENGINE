from flask import Blueprint, render_template

blueprint = Blueprint("controller", __name__)


@blueprint.route('/', methods=['POST', 'GET'])
def index():
    if "post":
        # "type >>java, python" = "choice of skills from client"

        pass
    return render_template('index.html')
