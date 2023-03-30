from contextlib import contextmanager
from sqlite3 import IntegrityError

from flask import render_template
from crewverve.models import db

@contextmanager
def transactional_session():
    session = db.session
    try:
        yield session
        session.commit()
    except (IntegrityError,AttributeError):
        session.rollback()
        raise
        #return render_template('error.html', error_message="error", error_description="No se ha podido grabar su respuesta, inténtelo más tarde")
    finally:
        session.close()