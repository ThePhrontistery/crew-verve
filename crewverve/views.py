from flask import Blueprint, redirect, render_template, request, session, url_for
from .data import create_answer, get_survey_by_id, get_user_by_name, get_pending_surveys_by_user, questions, show_result, transform_mood, update_survey_stats, update_ticket


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


@crewverve_bp.route('/crewverve/results', methods=['POST'])
def results():
#PL -INICIO- 21/03/2023   
    """results llama a tres métodos:
    1) save_results -> inserta una respuesta y actualiza estadísticas (pilar, laura)
    2) update_ticket -> da por completado un ticket por encuesta y usuario 
    3) show_results -> muestra la pantalla de estadísticas""" 
    resultado_save = False
    def save_results():
        "Estando en pantalla SURVEY, al dar al botón SAVE -> Graba en BBDD las respuestas y los calculos de las medias de esta encuesta y proyecto"
        #1.1 Obtenemos datos de pantalla con request.form (survey_id, mood (transformando valores) y rating-n)
        #id_survey = request.form['id_survey']
        id_survey = request.form['survey_id']
        mood_input = transform_mood(request.form['mood'])
        rating0_input = request.form['rating-0']
        rating1_input = request.form['rating-1']
        rating2_input = request.form['rating-2']
        rating3_input = request.form['rating-3']
        rating4_input = request.form['rating-4']
        rating5_input = request.form['rating-5']
        rating6_input = request.form['rating-6']
        rating7_input = request.form['rating-7']
        #1.2 Creamos answers como un string formado por la unión de la variable mood y las 8 variables rating_input y llamamos a la función create_answer(inserta en Survey_answers) 
        answers = f'{mood_input},{rating0_input},{rating1_input},{rating2_input},{rating3_input},{rating4_input},{rating5_input},{rating6_input},{rating7_input}'
        resultado_create = create_answer(id_survey, answers)
        #1.3 Actualizamos en la tabla Survey las estadísticas
        if resultado_create:
           survey = get_survey_by_id(id_survey)
           resultado_update = update_survey_stats(id_survey,survey.id_project)
           if resultado_update:
              return True
           
    resultado_save = save_results()
#PL -FIN- 21/03/2023

    if resultado_save:
        id_survey = request.form['survey_id']
        if update_ticket(session['CURRENT_USER'],id_survey):
            pass
            
            stat = show_result(session['CURRENT_USER'])
        else:
            return render_template('error.html', error_message="error", error_description="No se ha podido grabar su respuesta, inténtelo más tarde")
    else:
        return render_template('error.html', error_message="error", error_description="No se ha podido grabar su respuesta, inténtelo más tarde")
    return render_template('crewverve/results.html', stats=stat)

@crewverve_bp.route('/crewverve/results_footer', methods=['GET'])
def show_results_footer():
    stat = show_result(session['CURRENT_USER'])    
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
