from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime



## For referencing the file
app = Flask(__name__)

## Telling the app where the database is located
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'

## Initialize the database
db = SQLAlchemy(app)

## Creating a model for the db
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    def __repr__(self):
        return '<Task %r>' % self.id

## To set url route use :- @app.route('/') and define the function for the route

## route and fuction for the main index page
@app.route('/', methods=['POST','GET'])
def index():
    if request.method == 'POST':
        ## Addding the task on click on the form
        new_task = Todo(content=request.form['content'])

        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue adding your task!!!'
    else:
        tasks = Todo.query.order_by(Todo.date_created).all()
        return render_template('index.html', tasks=tasks)


## route and fuction for the main delete function
@app.route('/delete/<int:id>')
def delete(id):
    ## Adding the task on click on the form
    task_to_delete = Todo.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return f"There was an error deleting the task with task_id:{id}"

## route and fuction for the main update function
@app.route('/update/<int:id>', methods=['GET','POST'])
def update(id):
    ## Adding the task on click on the form
    task = Todo.query.get_or_404(id)

    if request.method == 'POST':
        try:
            task.content = request.form['content']
            db.session.commit()
            return redirect('/')
        except:
            return f'There was an issue Updating task with task_id:- {id} !!!'
    else:
        return render_template('update.html',task=task)


## To run the python code and set the port number
if __name__== "__main__":
    app.run(host="localhost", port=8000, debug=True)

