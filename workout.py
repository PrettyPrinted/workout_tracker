from flask import Flask, render_template, request, url_for, session, redirect, g, abort
from model import db, User, Exercises, Workout, Exercise, Set
from datetime import datetime
import bcrypt

app = Flask(__name__)
app.config['SECRET_KEY'] = 'DontTellAnyone!'

@app.before_request
def before_request():
    g.user = None
    if 'username' in session:
        g.user = session['username']

@app.route('/')
def index():
    if g.user:
        current_user = User.query.filter_by(name=g.user).first()

        workouts = current_user.workouts.order_by(Workout.date.desc()).all()

        return render_template('history.html', workouts=workouts)
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    user = User.query.filter_by(name=request.form['username'].encode('utf-8')).first()

    if user is not None:
        if bcrypt.hashpw(request.form['pass'].encode('utf-8'), user.password.encode('utf-8')) == user.password.encode('utf-8'):
            session['username'] = request.form['username']
            return redirect(url_for('index'))

        return 'Password is incorrect'

    return 'User does not exist!'

@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        pending_user = request.form['username'].encode('utf-8')

        username = User.query.filter_by(name=pending_user).first()

        if username is None:
            new_user = User(name=pending_user, password=bcrypt.hashpw(request.form['pass'].encode('utf-8'), bcrypt.gensalt()))
            db.session.add(new_user)
            db.session.commit()

            session['username'] = pending_user
            return redirect(url_for('index'))


    return render_template('register.html')

@app.route('/add_workout', methods=['POST', 'GET'])
def add_workout():
    if request.method == 'POST':
        user = User.query.filter_by(name=session['username']).first()

        workout = Workout(date=datetime.utcnow(), user_id=user.id)

        exercise_count = int(request.form['exercise_count'])

        for exercise_num in range(1,exercise_count + 1):
            exercise = Exercise(order=exercise_num, exercise_id=request.form['exercise'+str(exercise_num)], workout=workout)

            weights = request.form.getlist('weight' + str(exercise_num))
            reps = request.form.getlist('reps' + str(exercise_num))

            set_order = 1
            for weight, rep in zip(weights, reps):
                work_set = Set(order=set_order, exercise=exercise, weight=weight, reps=rep)
                set_order += 1

        db.session.add(workout)
        db.session.commit()

        return redirect(url_for('index'))

    exercises = Exercises.query.all()
    return render_template('add_workout.html', exercises=exercises)

@app.route('/logout')
def logout():
    session.pop('username')
    return redirect(url_for('index'))
