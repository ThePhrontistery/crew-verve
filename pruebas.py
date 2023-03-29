from crewverve.models import Survey, Survey_answer, Survey_ticket, User
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, delete, select, update
from sqlalchemy.orm.collections import InstrumentedList

# Set up the database connection (NO ES IGUAL A FLASK. NO ESTAMOS EN UN PROCESO DE FLASK AHORA!!!!)
engine = create_engine('sqlite:///./instance/crewverve.db')

# Create a new session factory
Session = sessionmaker(bind=engine)
session = Session()

def get_user_by_name(user_name):
    return session.execute(select(User).filter_by(name_user=user_name)).scalar_one_or_none()


def get_projects_by_user(user_name):
    "Get user (must exist) associated projects"
    user = get_user_by_name(user_name)
    return user.projects

if __name__ == '__main__':
    projects = get_projects_by_user('john')
    cosa = projects.index([i for i in projects][0])
    print(projects)
    cosa2 = [project for project in projects if project.id_project == 2]
    cosa1 = projects.index([project for project in projects if project.id_project == 2][0])
    print(cosa1)