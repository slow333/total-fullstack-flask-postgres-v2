from flask import Blueprint, render_template as render # type: ignore

bp = Blueprint('database_bp', __name__, url_prefix='/database')

@bp.route('/')
def database_home():
  return render('contents/database/00-database_index.html')

@bp.route('/datatype')
def database_datatype():
  return render('contents/database/01-datatype.html')

@bp.route('/crud')
def database_crud():
  return render('contents/database/02-crud.html')

@bp.route('/select')
def database_select():
  return render('contents/database/03-select.html')

@bp.route('/constraints')
def database_constraints():
  return render('contents/database/04-constraints.html')

@bp.route('/groupBy')
def database_groupBy():
  return render('contents/database/05-groupBy.html')

@bp.route('/join')
def database_join():
  return render('contents/database/06-join.html')

@bp.route('/aggregate')
def database_aggregate():
  return render('contents/database/07-aggregate.html')

@bp.route('/functions')
def database_functions():
  return render('contents/database/08-functions.html')

@bp.route('/procedureTrigger')
def database_procedure_trigger():
  return render('contents/database/09-procedure-trigger.html')
