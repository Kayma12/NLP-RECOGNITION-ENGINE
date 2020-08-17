import io
from flask import Blueprint, render_template, request, Response, make_response, send_file

import service
import data_plots

blueprint = Blueprint("controller", __name__)


@blueprint.route('/', methods=['POST', 'GET'])
def index():
    consultants = []
    skills = service.get_all_skills()
    consultants_in_db = service.check_if_database_is_not_empty()

    if request.method == 'POST':
        # If post request it returns a list of consultants based on the skills chosen

        select = request.form.getlist('vals')

        try:
            error_message = ""
            if len(select) > 0:
                consultants = service.query_consultants_with_skills(select)

                if len(consultants) < 1:
                    error_message = "There are no candidates available for selected criteria"
            else:
                error_message = "Please choose at least one skill!"

            return render_template('index.html', consultants=consultants, select=select, skills=skills,
                                   error_message=error_message, len_consultants=len(consultants), consultants_in_db=consultants_in_db)

        except:
            return "Please try again"
    else:
        # get request just shows the homepage with a list of skills to choose from

        # if db is empty return empty index page with a comment asking to fill db with consultants else render the
        # template with skills >> render_template('index.html', skills=skills, len_consultants=len(consultants))
        error_message_db_empty = "There are no consultants in the database"

        return render_template('index.html', skills=skills, len_consultants=len(consultants),
                               consultants_in_db=consultants_in_db, error_message_db_empty=error_message_db_empty)


@blueprint.route('/profile_page/<candidate_id>', methods=['POST', 'GET'])
def profile_page(candidate_id):
    consultant_details = service.get_consultant(candidate_id)

    if consultant_details.availability:
        consultant_details.availability = 'Yes'
    else:
        consultant_details.availability = 'No'
    return render_template('profile_page.html', consultant_details=consultant_details)


@blueprint.route('/send_image/<candidate_id>', methods=['POST', 'GET'])
def send_image(candidate_id):
    consultant_details = service.get_consultant(candidate_id)
    barchart_plot = data_plots.create_bar_chart(consultant_details.skills)
    img = io.BytesIO()
    barchart_plot.savefig(img)
    img.seek(0)
    return send_file(img, mimetype='image/png')


@blueprint.route('/download_link/<candidate_id>', methods=['POST', 'GET'])
def download_link(candidate_id):
    file = service.get_binary(candidate_id)
    response = make_response(file)
    response.headers['Content-Type'] = 'application/octet-stream'
    response.headers["Content-Disposition"] = "attachment; filename={}".format('candidate_cv.docx')
    return response
