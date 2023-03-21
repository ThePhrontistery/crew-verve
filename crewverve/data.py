from .models import Project, Survey, Survey_answer, Survey_ticket, db, User

questions = [
    "My enthusiasm regarding the work I do...",
    "The Teamwork atmosphere and communication during the last sprints were...",
    "To what extent the tasks were challenging enough for me...",
    "I would rate my value contributed to the team as follows...",
    "The workload of this/the last sprint was...",
    "I feel supported by the client and stakeholders...",
    "I feel recognized and praised by the team...",
    "I feel inspired and excited to work in this team for the coming sprints..."
]

# https://flask-sqlalchemy.palletsprojects.com/en/3.0.x/queries/
# https://docs.sqlalchemy.org/en/20/orm/queryguide/index.html

# PLP -INICIO- 17.03.2023
# Añado esta funcion del data de que-hacer para poder grabar contraseñas desde user_man
def find_user_by_name(user_name):
    "Searched for User from db by name. Needs not to exist"
    return db.session.execute(db.select(User).filter_by(name_user=user_name)).scalar_one_or_none()
# PLP -FIN- 17.03.2023

def get_user_by_id(user_id):
    return db.session.execute(db.select(User).filter_by(id_user=user_id)).scalar_one()

def get_user_by_name(user_name):
   
    return db.session.execute(db.select(User).filter_by(name_user=user_name)).scalar_one_or_none()

def get_projects_by_user(user_name):
    "Get user (must exist) associated projects"
    user = get_user_by_name(user_name)
    return user.projects

def get_pending_surveys_by_user(user_name):
    user = get_user_by_name(user_name)
    pending_survey = get_pending_survey_by_user(user.id_user)
    pending_survey_ids = [pending_survey.survey_id for pending_survey in pending_survey]

    active_surveys = get_active_surveys(pending_survey_ids)

    return active_surveys

def get_pending_survey_by_user(user_id):
    return db.session.execute(db.select(Survey_ticket)
                              .where(Survey_ticket.completed == False)
                              .where(Survey_ticket.user_id == user_id)).scalars().all()

def get_active_surveys(pending_survey_ids):
    return db.session.execute(db.select(Survey)
                              .where(Survey.id_survey.in_(pending_survey_ids))
                              .where(Survey.active)).scalars().all()

def get_active_survey_by_project_id(project_ids):
    return db.session.execute(db.select(Survey).where(Survey.id_project.in_(project_ids)))

#def save_results(id_survey):
    #pass
    #return ok_o_none

def get_results_stats(idsurvey, idproyect, iduser):

    #LGG modifico añadiendo pass

    pass
    #return results

def get_survey_by_id(survey_id):
    return db.session.execute(db.select(Survey).filter_by(id_survey=survey_id)).scalar_one_or_none()
#
def find_survey_ticket_by_id(user_id,survey_id):
    return db.session.execute(db.select(Survey_ticket).filter_by(user_id=user_id, survey_id=survey_id)).scalar_one_or_none()

def update_ticket(user_id,survey_id):
    ticket = find_survey_ticket_by_id(user_id,survey_id)
    ticket.completed = not ticket.completed
    db.session.commit()
    return ticket

#PL-INICIO- 21/03/2023
def get_answers_by_id(id_survey):
    "Recuperamos todas las filas de survey_answer únicamente la columna answers"
    return db.session.execute(db.select(Survey_answer.answers).where(Survey_answer.id_survey==id_survey)).scalars().all()

def get_users_by_project(id_project):
    "Recuperamos número de usuarios de un project"
    #return db.session.execute(db.select(Project).where(Project.id_project==id_project)).scalars().all()
    return db.session.execute(db.select(Project).filter_by(id_project=id_project)).scalar_one_or_none()

def transform_mood(mood):
    "transforma el mood recogido en syrvey.html (valores, 0,25,50,75,100) a valores 1,2,3,4,5"
    if mood == '100':
       return '5'
    elif mood == '75':
       return '4'
    elif mood =='50':
        return '3'
    elif mood == '25':
        return '2'
    else:
        return '1'    

def create_answer(id_survey, answers):
    "Create record in Survey_answer"
    answer = Survey_answer(id_survey=id_survey, answers=answers)
    db.session.add(answer)
    db.session.commit()
    return answer

def update_survey_stats(id_survey,id_project):
    "Actualizamos las estadísticas en la tabla Survey, pásandole el id_survey y el id_project"
    #en answer tengo ahora las columnas answer de las filas recuperadas en get_answers_by_id, solo recuperamos columna answers
    answer = get_answers_by_id(id_survey)
    #mood_total tiene el sumatorio de la primera ocurrencia de answer
    mood_total = sum(int(item_answer[0]) for item_answer in answer) 
    #participation_total tiene el número de participantes por cada id_survey
    participation_total = len(answer)
    #rating_total tiene el sumatorio de las ocurrencias de la 2 a la 16 de las filas recuperadas en get_answers_by_id
    rating_total = sum(int(item_answer[e]) for item_answer in answer for e in range(2,17,2)) 
    #Creo la función get_users_by_project y obtengo los usuarios por proyecto en user_total
    user = get_users_by_project(id_project)
    user_total = len(user.users)
    #nos posicionamos en el registro de la tabla Survey con el id_survey que estamos tratando
    survey = get_survey_by_id(id_survey)
    #mood es la media(total de mood entre el número de participantes)
    survey.mood = mood_total / participation_total
    #rating es la media(total de rating entre el número de participantes)
    survey.rating = rating_total / participation_total
    #participation es el número de usuario de projecto entre participantes
    survey.participation = participation_total*100 / user_total
    db.session.commit()
    return True
#PL -FIN- 21/03/2023   