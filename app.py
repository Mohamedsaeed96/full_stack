from flask import Flask, render_template,request,url_for,redirect
from flask_sqlalchemy import SQLAlchemy
import sys

app = Flask(__name__)
db = SQLAlchemy(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:123qwe@localhost:5432/todoapp'

class Todo(db.Model):
	__tablename__ = 'todos'
	id = db.Column(db.Integer, primary_key = True)
	description = db.Column(db.String(),nullable = False)

	def __repr__(self):
		return f'<Todo {self.id} {self.description}>'

db.create_all()

@app.route('/')
def index():
	return render_template('index.html', data=Todo.query.all())


@app.route('/todos/create', methods=['POST'])
def create_todo():
	error = False
	try:
		description = request.get_jason()['description']
		todo = Todo(description=description)
		db.session.add(todo)
		db.session.commit()
		
	except:
		error = True
		db.session.rollback()
		print(sys.exc_info)
	finally:
		db.session.close()
	if not error:
		return jsonify({'description': todo.description})