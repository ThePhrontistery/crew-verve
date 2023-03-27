from flask import Blueprint, redirect, render_template, request, session, url_for


from .data import get_survey_by_id, get_pending_surveys_by_user, questions, transform_mood, update_ticket, show_result, save_results


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
    #1.1 Obtenemos datos de pantalla con request.form (survey_id, mood (transformando valores) y rating-n)
    #id_survey = request.form['id_survey']
    id_survey = request.form['survey_id']
    mood_input = transform_mood(request.form['mood'])
    rating0 = request.form['rating-0']
    rating1 = request.form['rating-1']
    rating2 = request.form['rating-2']
    rating3 = request.form['rating-3']
    rating4 = request.form['rating-4']
    rating5 = request.form['rating-5']
    rating6 = request.form['rating-6']
    rating7 = request.form['rating-7']
    #1.2 Creamos answers como un string formado por la unión de la variable mood y las 8 variables rating_input y llamamos a la función create_answer(inserta en Survey_answers) 
    answers = f'{mood_input},{rating0},{rating1},{rating2},{rating3},{rating4},{rating5},{rating6},{rating7}'
    #1.3 En resultado_save guardamos el resultado del metodo save_results (true o False). 
    # Tiene los metodos 'create_answer' y 'update_survey_stats'
    resultado_save = save_results(id_survey,answers)

#PL -FIN- 21/03/2023

    if resultado_save:
        id_survey = request.form['survey_id']
        if update_ticket(session['CURRENT_USER'],id_survey): 
            survey = get_survey_by_id(id_survey)
            stat = show_result(session['CURRENT_USER'],survey.id_project,int(id_survey))
        else:
            return render_template('error.html', error_message="error", error_description="No se ha podido grabar su respuesta, inténtelo más tarde")
    else:
        return render_template('error.html', error_message="error", error_description="No se ha podido grabar su respuesta, inténtelo más tarde")
    return render_template('crewverve/results.html', stats=stat)

@crewverve_bp.route('/crewverve/results_footer', methods=['GET'])
def show_results_footer():
    if 'project_id' in request.args:
        id_project = request.args.get('project_id',type=int)
    else:
        id_project = 0
    
    if 'survey_id' in request.args:
        id_survey = request.args.get('survey_id',type=int)
    else:
        id_survey = 0
    stat = show_result(session['CURRENT_USER'],id_project,id_survey)    
    return render_template('crewverve/results.html', stats=stat)

