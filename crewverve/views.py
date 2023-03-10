from flask import Blueprint, redirect, render_template, request, session, url_for
from .data import questions


crewverve_bp = Blueprint('crewverve', __name__)


@crewverve_bp.route('/crewverve')
def index():

   
    return render_template('crewverve/index.html', pending_surveys=[])


@crewverve_bp.route('/crewverve/survey')
def survey():

    return render_template('crewverve/survey.html', questions=questions, survey=None)


@crewverve_bp.route('/crewverve/results')
def results():



    return render_template('crewverve/results.html', stats=[])

