from flask import Blueprint, flash, g, redirect, render_template, session, url_for
# from src.blueprints.auth import login_required
from src.db import get_db
import functools

bp = Blueprint('dashboard', __name__, url_prefix='/dashboard')

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)
    return wrapped_view


@bp.route('/index')
@login_required
def index():
    return render_template('dashboard/index.html')
