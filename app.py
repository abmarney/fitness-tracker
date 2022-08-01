from distutils.command.build_ext import extension_name_re
from flask import Flask, render_template, url_for, redirect, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

class Workout(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    routine = db.relationship('Exercise', backref='workout')

    def __repr__(self):
        return self.name

class Exercise(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String(200), nullable=False)
    reps=db.Column(db.Integer, nullable=False)
    sets=db.Column(db.Integer, nullable=False)
    workout_id=db.Column(db.Integer, db.ForeignKey('workout.id'))

    def __repr__(self):
        return self.name

@app.route('/')
def index():
    workouts=Workout.query.order_by(Workout.id).all()
    return render_template('index.html', workouts=workouts)

@app.route('/CreateWorkout/', methods=['POST','GET'])
def create_routine():
    workout_to_create=Workout.query.order_by(Workout.id).all()

    if request.method == 'POST':
        workout_name = request.form['name']
        new_workout = Workout(name=workout_name)

        try:
            db.session.add(new_workout)
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue creating your workout.'
    else:
        return render_template('workouts.html', workout=workout_to_create)

@app.route('/delete/<int:id>')
def routine_delete(id):
    workout_to_delete = Workout.query.get_or_404(id)

    try:
        db.session.delete(workout_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was a problem deleting this routine.'

@app.route('/workout/<int:id>')
def show_routine(id):
    workout_to_show = Workout.query.get_or_404(id)
    return render_template('workouts.html', workout=workout_to_show)

@app.route('/update/<int:id>', methods=['POST'])
def update_routine(id):
    workout_to_update = Workout.query.get_or_404(id)
    ex_name = request.form['name']
    ex_reps = request.form['reps']
    ex_sets = request.form['sets']
    new_exercise = Exercise(name=ex_name,reps=ex_reps,sets=ex_sets,workout=workout_to_update)

    try:
        db.session.add(new_exercise)
        db.session.commit()
        return redirect(f'/workout/{workout_to_update.id}')
    except:
        return 'There was a problem updating this workout.'

if __name__ == "__main__":
    app.run(debug=True)
