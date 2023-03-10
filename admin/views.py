
import os
from flask import Blueprint, render_template

admin_bp = Blueprint('admin', __name__)


@admin_bp.route('/admin')
def index():
    return render_template('admin/index.html')

