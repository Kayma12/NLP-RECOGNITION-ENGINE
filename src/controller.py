from flask import Blueprint, render_template, request
import service

blueprint = Blueprint("controller", __name__)


@blueprint.route('/', methods=['POST', 'GET'])
def index():
    consultants = []
    skills = service.get_all_skills()
    if request.method == 'POST':
        select = request.form.getlist('vals')
        error_message = ""
        try:
            if len(select) > 0:
                consultants = service.query_consultants_with_skills(select)

                if len(consultants) < 1:
                    error_message = "There are no CVs selected."
            else:
                error_message = "Please choose at least one skill!"

            return render_template('index.html', consultants=consultants, select=select, skills=skills,
                                   error_message=error_message, len_consultants=len(consultants))

        except:
            return "Please try again"
    else:
        return render_template('index.html', skills=skills, len_consultants=len(consultants))


@blueprint.route('/profile_page/<candidate_id>', methods=['POST', 'GET'])
def profile_page(candidate_id):
    consultant_details = service.get_consultant(candidate_id)

    if consultant_details.availability == True:
        consultant_details.availability = 'Yes'
    else:
        consultant_details.availability = 'No'

        # consultant_details.availability == true

    return render_template('profile_page.html', consultant_details=consultant_details)
