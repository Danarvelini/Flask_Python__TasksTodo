from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(255), nullable=False)
    
    def __repr__(self):
        return '<Task %r>' % self.id

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        requestedTask = request.form['content']
        newTask = Todo(content=requestedTask)
        
        try:
            db.session.add(newTask)
            db.session.commit()
            return redirect('/')
        except:
            return"Error adding task to Database"
    else:
        tasks = Todo.query.order_by(Todo.id).all()
        return render_template('index.html', tasks=tasks)
    
@app.route('/update/<int:id>', methods=['GET','POST'])
def update(id):
    task = Todo.query.get_or_404(id)
    
    if request.method == 'POST':
        task.content = request.form['content']
        try:
            db.session.commit()
            return redirect('/')
        except:
            return"Error updating your task"

    else:
        return render_template('update.html', task=task)
    
@app.route('/delete/<int:id>')
def delete(id):
    taskToDelete = Todo.query.get_or_404(id)
    try:
        db.session.delete(taskToDelete)
        db.session.commit()
        return redirect('/')
    except:
        return"Error deleting your task"

if __name__ == '__main__':
    app.run(debug=True)