from flask import Blueprint, redirect, render_template, request, session, url_for
from .data import get_survey_by_id, get_user_by_name, get_pending_surveys_by_user, questions, show_result


crewverve_bp = Blueprint('crewverve', __name__)


@crewverve_bp.route('/crewverve')
def index():
    pending_surveys = get_pending_surveys_by_user(session['CURRENT_USER'])
    return render_template('crewverve/index.html', pending_surveys=pending_surveys)


@crewverve_bp.route('/crewverve/survey', methods=['POST'])
def survey():
    id_survey = request.form['survey_id']
    survey = get_survey_by_id(id_survey)
    return render_template('crewverve/survey.html', questions=questions, survey=survey)


@crewverve_bp.route('/crewverve/results_footer', methods=['POST','GET'])
def show_results_footer():

    stat = show_result()
    print (stat)
    return render_template('crewverve/results.html', stats=stat)


""" def results():
    save():
        - grabar en BBDD las respuestas y los calculos de la pantalla RESULTS  de esta encuesta y proyecto
        - actualizar el ticket de usuario marcarlo como realizado

    #show results 
     if request.endpoint not in ('survey')
        show_results()
    else
    stats = []
    if save():
        if update_ticket():
            stats = show_results()
        else:
            return render_template('error.html', error_message="error", error_description="This isn't the page you are looking for....")
    else:
        return render_template('error.html', error_message="error", error_description="This isn't the page you are looking for....")
    return render_template('crewverve/results.html', stats=stats) """
