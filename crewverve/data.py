from .models import Project, Survey, Survey_answer, Survey_ticket, db, User, Stats


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

def get_survey_by_id(survey_id):
    return db.session.execute(db.select(Survey).filter_by(id_survey=survey_id)).scalar_one_or_none()
#
def find_survey_ticket_by_id(user_id,survey_id):
    return db.session.execute(db.select(Survey_ticket).filter_by(user_id=user_id, survey_id=survey_id)).scalar_one_or_none()

def update_ticket(user_name,survey_id):
    user = get_user_by_name(user_name)
    ticket = find_survey_ticket_by_id(user.id_user,survey_id)
    ticket.completed = not ticket.completed
    return db.session.execute(db.update(Survey_ticket).where(Survey_ticket.user_id == user.id_user)
                              .where(Survey_ticket.survey_id == survey_id)
                              .values(completed=ticket.completed))

def find_position_projects(id,projects):
    return projects.index([project for project in projects if project.id_project == id][0])
        
def find_position_surveys(id,surveys):
    return surveys.index([survey for survey in surveys if survey.id_survey == id][0])

def show_result(user_name, id_project, id_survey):
    
    #Se define objeto de la clase Stats
    stat = Stats()
    #Se recuperan los proyectos por usuario
    stat.projects = get_projects_by_user(user_name)

    #Si solo viene informada la encuesta, se accede a recuperar el id de proyecto
    if id_project == 0 and id_survey != 0:
        stat.survey = get_survey_by_id(id_survey)
        id_project = stat.survey.id_project

    #Si no ha seleccionado un proyecto, se iguala el primero que se encuentra
    if id_project == 0:
        try:
            id_project = stat.projects[0].id_project
        except:
            return 0
    
    for project in stat.projects:
        #Se recuperan las encuestas del proyecto seleccionado
        if project.id_project == id_project:
            stat.surveys = sorted(project.surveys,key=lambda x:x.start_date)
            break
    #Para que se cargue el proyecto que se ha seleccionado, buscamos la posición que ocupa
    #dentro del combo y es la que le pasamos.
    stat.selected_project = find_position_projects(id_project,stat.projects)

    try:
        stat.survey_has_answers = -1
        #Se comprueba si tiene datos la clase survey
        if stat.surveys[0].id_survey != 0:
            #Si tiene datos, se comprueba si han seleccionado alguna encuesta
            if id_survey != 0:
                #Se iguala a la seleccionada
                stat.selected_survey = find_position_surveys(id_survey,stat.surveys)
                stat.survey = stat.surveys[stat.selected_survey]
            else:
                #Se iguala a la primera encuesta encontrada
                stat.selected_survey = 0
                stat.survey = stat.surveys[0]
            if len(stat.survey.answers) > 0:
                stat.survey_has_answers = 1
        else:
            #Si no tiene datos, es que el proyecto no tiene encuestas seleccionadas
            stat.selected_survey = -1
            stat.survey_has_answers = -1
    except Exception:
        #Salta la excepción en caso que no tenga encuestas el proyecto
        stat.selected_survey = -1
        stat.survey_has_answers = -1
        stat.survey = Survey (mood= 0, rating = 0, participation = 0)
        stat.surveys = []
    return stat


def save_results(id_survey,answers, username):
    "Estando en pantalla SURVEY,al dar al botón SAVE->Graba en BBDD las respuestas y los calculos de las medias de esta encuesta y proyecto y actualiza el ticket"
    try:
        #En resultado_create guardamos el resultado del metodo create_answer (true o False) que inserta en 'Survey_answer'
        create_answer(id_survey, answers)
        #Actualizamos en la tabla Survey las estadísticas
        update_survey_stats(get_survey_by_id(id_survey))
        update_ticket(username,id_survey)
        db.session.commit()
        return True
    except:
        db.session.rollback()
        return False
        
def get_answers_by_id(id_survey):
    "Recuperamos todas las filas de survey_answer únicamente la columna answers"
    return db.session.execute(db.select(Survey_answer.answers).where(Survey_answer.id_survey==id_survey)).scalars().all()

def get_users_by_project(id_project):
    "Recuperamos número de usuarios de un project"
    #return db.session.execute(db.select(Project).where(Project.id_project==id_project)).scalars().all()
    return db.session.execute(db.select(Project).filter_by(id_project=id_project)).scalar_one_or_none()

def transform_mood(mood):
    "transforma el mood recogido en survey.html (valores, 0,25,50,75,100) a valores 1,2,3,4,5"
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
    return db.session.add(answer)

    
def update_survey_stats(survey):
    "Actualizamos las estadísticas en la tabla Survey, pásandole el id_survey y el id_project"
    #en answer tengo ahora las columnas answer de las filas recuperadas en get_answers_by_id, solo recuperamos columna answers
    answer = get_answers_by_id(survey.id_survey)
    #mood_total tiene el sumatorio de la primera ocurrencia de answer
    mood_total = sum(int(item_answer[0]) for item_answer in answer) 
    #participation_total tiene el número de participantes por cada id_survey
    participation_total = len(answer)
    #rating_total tiene el sumatorio de las ocurrencias de la 2 a la 16 de las filas recuperadas en get_answers_by_id
    rating_total = sum(int(item_answer[e]) for item_answer in answer for e in range(2,17,2)) 
    #Creo la función get_users_by_project y obtengo los usuarios por proyecto en user_total
    user = get_users_by_project(survey.id_project)
    user_total = len(user.users)
    #mood es la media(total de mood entre el número de participantes)
    survey.mood = mood_total / participation_total
    #rating es la media(total de rating entre el número de participantes)
    survey.rating = rating_total / (participation_total*8)
    #participation es el número de usuario de projecto entre participantes
    survey.participation = participation_total*100 / user_total
    return db.session.execute(db.update(Survey).where(Survey.id_survey == survey.id_survey)
                              .values(mood=survey.mood, rating=survey.rating, participation= survey.participation))
 
