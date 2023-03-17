from .models import Survey, Survey_ticket, db, User

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

def save_results(id_survey):
    #LGG modifico añadiendo pass
    pass
    #return ok_o_none

def update_ticket(idsurvey, iduser):
    #LGG modifico añadiendo pass
    pass
    #return ok_o_none

def get_results_stats(idsurvey, idproyect, iduser):
    #LGG modifico añadiendo pass
    pass
    #return results

def get_survey_by_id(survey_id):
    return db.session.execute(db.select(Survey).filter_by(id_survey=survey_id)).scalar_one_or_none()



