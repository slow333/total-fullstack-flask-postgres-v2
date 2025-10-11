from flask import Blueprint, render_template


bp = Blueprint('main_home', __name__)

@bp.route('/')
@bp.route('/home')
def main_home():
  return render_template('index.html')

@bp.route('/apps/')
def apps_home():
  return render_template('apps/apps_home.html')