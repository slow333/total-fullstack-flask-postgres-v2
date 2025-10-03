from flask import Blueprint, render_template as render # type: ignore

bp = Blueprint('python_bp', __name__, url_prefix='/python')

@bp.route('/')
def python_home():
  return render('contents/python/python_index.html')

# python basic ================================
@bp.route('/core/')
@bp.route('/core/datatype')
def python_datatype():
  return render('contents/python/core/01_datatype.html')

@bp.route('/core/print-format')
def python_print_format():
  return render('contents/python/core/02_print_format.html')

@bp.route('/core/loop')
def python_loop():
  return render('contents/python/core/03_loop.html')

@bp.route('/core/def-file')
def python_def_file():
  return render('contents/python/core/04_def_file.html')

@bp.route('/core/class-module')
def python_class_module():
  return render('contents/python/core/05_class_module.html')

@bp.route('/core/try-except')
def python_try_except():
  return render('contents/python/core/06_try_except.html')

@bp.route('/core/py-library')
def python_py_library():
  return render('contents/python/core/07_py_library.html')

@bp.route('/core/closer-decorator')
def python_closer_decorator():
  return render('contents/python/core/08_closer_decorator.html')

@bp.route('/core/regexp')
def python_regexp():
  return render('contents/python/core/09_regexp.html')

# python adv ================================
@bp.route('/adv/')
@bp.route('/adv/01_class')
def python_adv_class():
  return render('contents/python/adv/01_class.html')

@bp.route('/adv/02_moudle')
def python_adv_moudle():
  return render('contents/python/adv/02_moudle.html')

@bp.route('/adv/03_try_except')
def python_adv_try_except():
  return render('contents/python/adv/03_try_except.html')

@bp.route('/adv/04_py_library')
def python_adv_py_library():
  return render('contents/python/adv/04_py_library.html')

@bp.route('/adv/05_closer_decorator')
def python_adv_closer_decorator():
  return render('contents/python/adv/05_closer_decorator.html')

@bp.route('/adv/06_regexp')
def python_adv_regexp():
  return render('contents/python/adv/06_regexp.html')


# python flask ================================
@bp.route('/flask/')
@bp.route('/flask/db-setup')
def flask_db_setup():
  return render('contents/python/flask/db_setup.html')

@bp.route('/flask/core-crud')
def flask_core_crud():
  return render('contents/python/flask/core_crud.html')

@bp.route('/flask/install')
def flask_install():
  return render('contents/python/flask/install.html')

@bp.route('/flask/note')
def flask_note():
  return render('contents/python/flask/note.html')