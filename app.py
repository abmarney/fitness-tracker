from flask import Flask, render_template, url_for, redirect, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)
exercise_count = 0

class Exercise(db.Model):
    name = db.Column(db.String(200), primary_key=True)
    reps = db.Column(db.Integer)
    sets = db.Column(db.Integer)
    #id = db.Column(db.Integer)
    def __repr__(self):
        return self.name

class Workout(db.Model):
    name = db.Column(db.String(200), primary_key=True)
    #routine = [Exercise()]
    #count = len(routine)
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

@app.route('/delete/Exercise/<string:name>')
def exercise_delete(name):
    exercise_to_delete = Exercise.query.get_or_404(name)

    try:
        db.session.delete(exercise_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was a problem deletingg this exercise.'

@app.route('/update/Exercise/<string:name>', methods=['POST','GET'])
def exercise_update(name):
    exercise_to_update = Exercise.query.get_or_404(name)

    if request.method == 'POST':
        exercise_to_update.name = request.form['name']
        exercise_to_update.reps = request.form['reps']
        exercise_to_update.sets = request.form['sets']

        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue updating this exercise.'
    else:
        return render_template('update.html', exercise=exercise_to_update)

if __name__ == "__main__":
    app.run(debug=True)
