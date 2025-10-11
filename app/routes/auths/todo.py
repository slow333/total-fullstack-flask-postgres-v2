from flask import Blueprint, render_template, request, redirect, url_for, flash
from ...extensions import db
from ...models import Todo
from .utils import pagenation
from flask_login import login_required, current_user

bp = Blueprint('todo_app', __name__, url_prefix='/apps/todos')

@bp.route('/')
def todo_home():
  # query_result, page, per_page, total_pages, page_len, start_page,end_page
  pagination_data = pagenation(Todo)

  return render_template("apps/todo/todo_home.html", 
              todos=pagination_data['query_result'], 
              per_page=pagination_data['per_page'], 
              page=pagination_data['page'], 
              total_pages=pagination_data['total_pages'], 
              start_page=pagination_data['start_page'], 
              end_page=pagination_data['end_page'], 
              page_len=pagination_data['page_len'])

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
        return redirect(url_for('todo_app.todo_home'))
    
    db.session.add(Todo(content=content, title=title, created=created, completed=completed, user_id=current_user.id))
    db.session.commit()
    
    return redirect(url_for('todo_app.todo_home'))
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
    
    return redirect(url_for('todo_app.todo_home'))

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

    return redirect(url_for('todo_app.todo_home'))