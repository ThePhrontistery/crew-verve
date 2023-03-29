from crewverve.models import Survey, Survey_answer, Survey_ticket
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, delete, update

# Set up the database connection (NO ES IGUAL A FLASK. NO ESTAMOS EN UN PROCESO DE FLASK AHORA!!!!)
engine = create_engine('sqlite:///./instance/crewverve.db')

# Create a new session factory
Session = sessionmaker(bind=engine)

def reset_database():
    delete_all_answers()
    reset_all_tickets()
    reset_all_surveys()
    return


def delete_all_answers():
    return session.execute(delete(Survey_answer))

def reset_all_tickets():
    #return session.execute(update(Survey_ticket).where(Survey_ticket.completed == 1).values({"completed": 0}))
    return session.execute(update(Survey_ticket).values({"completed": 0}))

def reset_all_surveys():
    return session.execute(update(Survey).values({"mood": 0}).values({"rating": 0}).values({"participation": 0}))



if __name__ == '__main__':
    session = Session()
    try:
        reset_database()
        session.commit()
    except:
        session.rollback()