from flask import Flask, request, jsonify, make_response
from flask_migrate import Migrate
from marshmallow import ValidationError
from datetime import datetime

from config import DATABASE_URI
from models import db, Workout, Exercise, WorkoutExercise
from schemas import (
    workout_schema, 
    workouts_schema, 
    exercise_schema, 
    exercises_schema, 
    workout_exercise_schema
)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)
db.init_app(app)

# Helper for 404 Response
def not_found(resource="Resource"):
    return make_response(jsonify({"error": f"{resource} not found"}), 404)


# --- WORKOUT ROUTES ---

@app.route('/workouts', methods=['GET'])
def get_workouts():
    workouts = Workout.query.all()
    return make_response(workouts_schema.dump(workouts), 200)


@app.route('/workouts/<int:id>', methods=['GET'])
def get_workout_by_id(id):
    workout = Workout.query.filter_by(id=id).first()
    if not workout:
        return not_found("Workout")
    return make_response(workout_schema.dump(workout), 200)


@app.route('/workouts', methods=['POST'])
def create_workout():
    json_data = request.get_json()
    if not json_data:
        return make_response(jsonify({"error": "No input data provided"}), 400)
    
    try:
        # Schema Validation & Deserialization
        data = workout_schema.load(json_data)
        new_workout = Workout(
            date=data['date'],
            duration_minutes=data['duration_minutes'],
            notes=data.get('notes')
        )
        db.session.add(new_workout)
        db.session.commit()
        return make_response(workout_schema.dump(new_workout), 201)
    
    except ValidationError as err:
        return make_response(jsonify({"errors": err.messages}), 422)
    except ValueError as err:
        db.session.rollback()
        return make_response(jsonify({"error": str(err)}), 422)


@app.route('/workouts/<int:id>', methods=['DELETE'])
def delete_workout(id):
    workout = Workout.query.filter_by(id=id).first()
    if not workout:
        return not_found("Workout")
    
    # Associated WorkoutExercises deleted automatically due to cascade="all, delete-orphan"
    db.session.delete(workout)
    db.session.commit()
    return make_response(jsonify({"message": "Workout successfully deleted"}), 200)


# --- EXERCISE ROUTES ---

@app.route('/exercises', methods=['GET'])
def get_exercises():
    exercises = Exercise.query.all()
    return make_response(exercises_schema.dump(exercises), 200)


@app.route('/exercises/<int:id>', methods=['GET'])
def get_exercise_by_id(id):
    exercise = Exercise.query.filter_by(id=id).first()
    if not exercise:
        return not_found("Exercise")
    
    # Build customized response returning exercise with associated workouts
    result = exercise_schema.dump(exercise)
    result['workouts'] = workouts_schema.dump(exercise.workouts)
    return make_response(jsonify(result), 200)


@app.route('/exercises', methods=['POST'])
def create_exercise():
    json_data = request.get_json()
    if not json_data:
        return make_response(jsonify({"error": "No input data provided"}), 400)
    
    try:
        data = exercise_schema.load(json_data)
        new_exercise = Exercise(
            name=data['name'],
            category=data['category'],
            equipment_needed=data['equipment_needed']
        )
        db.session.add(new_exercise)
        db.session.commit()
        return make_response(exercise_schema.dump(new_exercise), 201)
    
    except ValidationError as err:
        return make_response(jsonify({"errors": err.messages}), 422)
    except ValueError as err:
        db.session.rollback()
        return make_response(jsonify({"error": str(err)}), 422)


@app.route('/exercises/<int:id>', methods=['DELETE'])
def delete_exercise(id):
    exercise = Exercise.query.filter_by(id=id).first()
    if not exercise:
        return not_found("Exercise")
    
    # Associated WorkoutExercises deleted automatically due to cascade="all, delete-orphan"
    db.session.delete(exercise)
    db.session.commit()
    return make_response(jsonify({"message": "Exercise successfully deleted"}), 200)


# --- JOIN TABLE ROUTE (ADD EXERCISE TO WORKOUT) ---

@app.route('/workouts/<int:workout_id>/exercises/<int:exercise_id>/workout_exercises', methods=['POST'])
def add_exercise_to_workout(workout_id, exercise_id):
    workout = Workout.query.filter_by(id=workout_id).first()
    if not workout:
        return not_found("Workout")
    
    exercise = Exercise.query.filter_by(id=exercise_id).first()
    if not exercise:
        return not_found("Exercise")

    json_data = request.get_json() or {}

    try:
        data = workout_exercise_schema.load(json_data)
        
        workout_exercise = WorkoutExercise(
            workout_id=workout.id,
            exercise_id=exercise.id,
            reps=data.get('reps'),
            sets=data.get('sets'),
            duration_seconds=data.get('duration_seconds')
        )

        db.session.add(workout_exercise)
        db.session.commit()

        return make_response(workout_exercise_schema.dump(workout_exercise), 201)

    except ValidationError as err:
        return make_response(jsonify({"errors": err.messages}), 422)
    except ValueError as err:
        db.session.rollback()
        return make_response(jsonify({"error": str(err)}), 422)


if __name__ == '__main__':
    app.run(port=5555, debug=True)