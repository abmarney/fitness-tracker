from distutils.command.build_ext import extension_name_re
from flask import Flask, render_template, url_for, redirect, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

#Class: Workout
# A class to hold the workout's name and collection of exercise objects.
#
class Workout(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    routine = db.relationship('Exercise', backref='workout')

    def __repr__(self):
        return self.name

# Class: Exercise
# A class to hold an exercises name, current relevent detatils, and attach it to a specific workout.
#
class Exercise(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String(200), nullable=False)
    reps=db.Column(db.Integer, nullable=False)
    sets=db.Column(db.Integer, nullable=False)
    workout_id=db.Column(db.Integer, db.ForeignKey('workout.id'))

    def __repr__(self):
        return self.name

# Home
# Currently displays existing workouts so the user can update or delete them, and allows the user to create a new workout.
#
@app.route('/')
def index():
    workouts=Workout.query.order_by(Workout.id).all()
    return render_template('index.html', workouts=workouts)

########### WORKOUT METHODS ###########

# Create Workout
# Currently handles taking input for creating a new workout.
# name = name for the new workout.
#
@app.route('/CreateWorkout/', methods=['POST','GET'])
def create_workout():
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

# Delete workout
# Deletes a workout after a button press by the user using it's id.
# id = id of the workout to be deleted
#
@app.route('/delete/<int:id>')
def delete_workout(id):
    workout_to_delete = Workout.query.get_or_404(id)

    try:
        db.session.delete(workout_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was a problem deleting this routine.'

# Display Workout
# Displays a selected workout's exercises and relevent information.
# id = id of the workout to be displayed
#
@app.route('/workout/<int:id>')
def show_workout(id):
    workout_to_show = Workout.query.get_or_404(id)
    return render_template('workouts.html', workout=workout_to_show)

########### EXERCISE METHODS ###########

# Update Workout
# Adds exercises for the currently selected workout
# id = id of the workout to be updated
#
@app.route('/update/<int:id>', methods=['POST'])
def update_workout(id):
    workout_to_update = Workout.query.get_or_404(id)
    ex_name = request.form['name']
    ex_reps = request.form['reps']
    ex_sets = request.form['sets']
    new_exercise = Exercise(
        name=ex_name,
        reps=ex_reps,
        sets=ex_sets,
        workout=workout_to_update
        )

    try:
        db.session.add(new_exercise)
        db.session.commit()
        return redirect(f'/workout/{workout_to_update.id}')
    except:
        return 'There was a problem updating this workout.'

# Delete Exercise
# Deletes a user selected exercise from the currently accessed workout.
# id = id of the exercise to be deleted.
#
@app.route('/workout/delete/<int:id>')
def delete_exercise(id):
    exercise_to_delete = Exercise.query.get_or_404(id)
    workout_to_update = exercise_to_delete.workout_id
    try:
        db.session.delete(exercise_to_delete)
        db.session.commit()
        return redirect(f'/workout/{workout_to_update}')
    except:
        return 'There was a problem removing this exercise.'

# Update Exercise [IN DEV]
# Updates a user selected exercise from the currently accessed workout.
# id = id of the exercise to be deleted.
#
@app.route('/workout/update/<int:id>')
def update_exercise(id):
    exercise_to_update = Exercise.query.get_or_404(id)
    workout_to_update = exercise_to_update.workout_id
    try:
        pass
    except:
        pass

if __name__ == "__main__":
    app.run(debug=True)