from flask import Blueprint, render_template, request, redirect, url_for, flash
from ... import db
from ...models import Todo

bp = Blueprint('todo', __name__, url_prefix='/apps/todo')

@bp.route('/')
def index():
  todos = Todo.query.all()
  return render_template('apps/todo/todo_index.html', todos=todos)

@bp.route('/add', methods=['POST'])
def add_todo():
  content = request.form.get('content')
  if not content:
      flash("할 일을 입력해주세요.")
      return redirect(url_for('todo.index'))
  
  new_todo = Todo(content=content)
  db.session.add(new_todo)
  db.session.commit()
  
  return redirect(url_for('todo.index'))
 
@bp.route('/update/<int:todo_id>')
def update_todo(todo_id):
  todo = Todo.query.get_or_404(todo_id)
  todo.completed = not todo.completed
  db.session.commit()
  
  return redirect(url_for('todo.index'))

@bp.route('/delete/<int:todo_id>')
def delete_todo(todo_id):
  todo = Todo.query.get_or_404(todo_id)
  db.session.delete(todo)
  db.session.commit()

  return redirect(url_for('todo.index'))