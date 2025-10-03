from . import db

class BaseModel(db.Model):
  __abstract__ = True
  __allow_unmapped__ = True
  id = db.Column(db.Integer, primary_key=True, autoincrement=True)

class Todo(BaseModel):
  content = db.Column(db.String(200), nullable=False)
  completed = db.Column(db.Boolean, default=False)

  def __repr__(self):
    return f'<Todo {self.id}>'