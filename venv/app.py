from flask import Flask, render_template,redirect,request, url_for,jsonify
from flask_sqlalchemy import SQLAlchemy

# app
app = Flask(__name__)

# database
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:toor@localhost:5432/Flask_Todo"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)
app.app_context().push()

# create table
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(1000), nullable=False)
db.create_all()  

@app.route('/')
def home():
    content = Todo.query.all()
    return render_template('todo.html', content = content)

@app.route('/insert_todo', methods = ['POST', 'GET'])
def insert_todo():
    if request.method == 'POST':
        content = request.form['content']
        newContent = Todo(content = content)
        db.session.add(newContent)
        db.session.commit()
        content = Todo.query.all()
        return render_template('todo.html', content=content)
    else:
        return render_template('todo.html')
    
@app.route('/delete/<int:id>', methods = ['POST', 'GET'])
def delete_todo(id):
    todo = Todo.query.filter_by(id= id).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for('home'))

@app.route('/update/<int:id>', methods = ['POST', 'GET'])
def update(id):
    todo = Todo.query.filter_by(id= id).first()
    print('bla bla', todo, type(todo))
    updateContent = []
    for column in todo.__table__.columns:
        updateContent.append(getattr(todo, column.name))
    jsonify(updateContent)
    return render_template('update.html',updateContent=updateContent )


     
@app.route('/edit/<int:id>', methods = ['POST', 'GET'])
def edit(id):
    if request.method == 'POST':
        todo = Todo.query.filter_by(id = id).first()
        todo.content = request.form['updatecontent']
        db.session.commit()
        updateTodo = Todo.query.all()
        return render_template('todo.html', content=updateTodo )
    