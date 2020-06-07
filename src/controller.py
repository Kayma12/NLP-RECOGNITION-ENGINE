from flask import Blueprint, render_template, request
import service

blueprint = Blueprint("controller", __name__)


@blueprint.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        # "type >>java, python" = "choice of skills from client"
        list_items = ""
        try:
            consultants = service.query_skills(list_items)
            return render_template('index.html', consultants=consultants)
        except:
            return "No skills were added, or no candidates met your criteria!"
    else:
        # we need to get all skills from db to display at front
        skills = service.get_all_skills()

        return render_template('index.html', skills=skills)
