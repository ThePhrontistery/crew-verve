from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker
from .crewverve.models import Survey_answer
from .crewverve.data import create_answer
# Set up the database connection (NO ES IGUAL A FLASK. NO ESTAMOS EN UN PROCESO DE FLASK AHORA!!!!)
engine = create_engine('sqlite:///./instance/crewverve.db')
Session = sessionmaker(bind=engine)
session = Session()

create_answer(None,None)