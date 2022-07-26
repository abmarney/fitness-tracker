from flask import Flask, render_template, url_for, redirect, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

class Exercise(db.Model):
    name = db.Column(db.String(200), primary_key=True)
    reps = db.Column(db.Integer)
    sets = db.Column(db.Integer)
    def __repr__(self):
        return self.name

class Workout(db.Model):
    name = db.Column(db.String(200), primary_key=True)
    def __repr__(self):
        return self.name

@app.route('/', methods=['POST','GET'])
def index():
    if request.method == 'POST':
        ex_name = request.form['name']
        ex_reps = request.form['reps']
        ex_sets = request.form['sets']
        new_exercise = Exercise(name=ex_name,reps=ex_reps,sets=ex_sets)
        
        try:
            db.session.add(new_exercise)
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an error creating your exercise'
    else:
        exercises=Exercise.query.order_by(Exercise.name).all()
        return render_template('index.html', exercises=exercises)

if __name__ == "__main__":
    app.run(debug=True)


