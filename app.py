from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class todolist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    completed = db.Column(db.Boolean, default=False)
    date_completed = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Task %r>' % self.id

@app.route('/')
def index():
    todoget = todolist.query.all()

    print(todoget[0].content)
    return render_template('index.html', todoget=todoget)

@app.route('/add', methods=['POST'])
def add():
    content = request.form['content']
    if not content:
        return redirect(url_for('index'))
    new_todo = todolist(content=content)
    db.session.add(new_todo)
    db.session.commit()
    return redirect(url_for('index'))


@app.route('/complete/<int:id>')
def complete(id):
    new_todo = todolist.query.filter_by(id=id).first()
    new_todo.completed = True
    db.session.commit()
    return redirect(url_for('index'))


@app.route('/delete/<int:id>')
def delete(id):
    new_todo = todolist.query.filter_by(id=id).first()
    db.session.delete(new_todo)
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  
    app.run(debug=True)

