from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///todo.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Todo(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    desc = db.Column(db.String(500), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"{self.sno} - {self.title}"

# Rename the route function to 'index'
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        title = request.form['title']
        desc = request.form['desc']
        # Create a new Todo item
        todo = Todo(title=title, desc=desc)
        db.session.add(todo)
        db.session.commit()
        return redirect(url_for('index'))

    # Fetch all todo items for GET requests
    alltodo = Todo.query.all()
    return render_template('index.html', alltodo=alltodo)

@app.route('/Products')
def Products():
    alltodo = Todo.query.all()
    print(alltodo)
    return 'This is my products.'

@app.route('/Products/Sami')
def Sami():
    return 'This is my Name.'

@app.route('/delete/<int:sno>')
def delete(sno):
    todo = Todo.query.filter_by(sno=sno).first()
    if todo:
        db.session.delete(todo)
        db.session.commit()
    return redirect(url_for('index'))  # Redirect to 'index'

@app.route('/update/<int:sno>', methods=['GET', 'POST'])
def update(sno):
    todo = Todo.query.filter_by(sno=sno).first()
    if request.method == 'POST':
        todo.title = request.form['title']
        todo.desc = request.form['desc']
        db.session.commit()
        return redirect(url_for('index'))  # Redirect to 'index'
    return render_template('update.html', todo=todo)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        print("Database and tables created!")  # Fixed indentation
    app.run(debug=True)
