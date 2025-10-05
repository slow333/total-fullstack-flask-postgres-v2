from flask import Blueprint, render_template, request, redirect, url_for, flash
from ... import db
from ...models import Todo
from .utils import pagenation
from flask_login import login_required, current_user

bp = Blueprint('todo', __name__, url_prefix='/apps/todos')

@bp.route('/')
def index():
  page, profile_page, total_pages, page_len, start_page, end_page = pagenation(Todo)
  todos = Todo.query.all()

  return render_template("apps/todo/todo_home.html", 
                todos=todos, 
                profiles=profile_page, 
                page=page, 
                total_pages=total_pages, 
                start_page=start_page, 
                end_page=end_page, 
                profile_page_len=page_len)

@bp.route('/create', methods=['POST', 'GET'])
@login_required
def add_todo():
  if request.method == 'POST':
    title = request.form.get('title')
    content = request.form.get('content')
    created = request.form.get('created')
    completed = request.form.get('completed')

    if not title and not content:
        flash("타일틀과 내용을 입력해주세요.")
        return redirect(url_for('todo.index'))
    
    db.session.add(Todo(content=content, title=title, created=created, completed=completed, user_id=current_user.id))
    db.session.commit()
    
    return redirect(url_for('todo.index'))
  else:
    return render_template('apps/todo/create_todo.html')
 
@bp.route('/update/<int:todo_id>', methods=['POST', 'GET'])
@login_required
def update_todo(todo_id):
  if request.method == 'GET':
    todo = Todo.query.get_or_404(todo_id)
    return render_template('apps/todo/update_todo.html', todo=todo)
  else:
    title = request.form.get('title')
    content = request.form.get('content')
    created = request.form.get('created')
    # completed = request.form.get('completed')

    todo = Todo.query.get_or_404(todo_id)
    todo.title = title
    todo.content = content
    todo.created = created
    todo.completed = not todo.completed
    db.session.commit()
    
    return redirect(url_for('todo.index'))

@bp.route('/delete/<int:todo_id>', methods=['POST', 'GET'])
@login_required
def delete_todo(todo_id):
  if request.method == 'GET':
    todo = Todo.query.get_or_404(todo_id)
    return render_template('apps/todo/delete_todo.html', todo=todo)
  else:
    todo = Todo.query.get_or_404(todo_id)
    db.session.delete(todo)
    db.session.commit()

    return redirect(url_for('todo.index'))