#!/usr/bin/env python3

from datetime import date
from app import app
from models import db, Workout, Exercise, WorkoutExercise

with app.app_context():
    print("Clearing database...")
    WorkoutExercise.query.delete()
    Workout.query.delete()
    Exercise.query.delete()

    print("Seeding exercises...")
    e1 = Exercise(name="Push-ups", category="Strength", equipment_needed=False)
    e2 = Exercise(name="Treadmill Run", category="Cardio", equipment_needed=True)
    e3 = Exercise(name="Barbell Squat", category="Strength", equipment_needed=True)
    e4 = Exercise(name="Plank", category="Balance", equipment_needed=False)

    db.session.add_all([e1, e2, e3, e4])
    db.session.commit()

    print("Seeding workouts...")
    w1 = Workout(date=date(2026, 7, 20), duration_minutes=45, notes="Upper body focus")
    w2 = Workout(date=date(2026, 7, 22), duration_minutes=60, notes="Leg day & Cardio")

    db.session.add_all([w1, w2])
    db.session.commit()

    print("Seeding workout exercises...")
    we1 = WorkoutExercise(workout_id=w1.id, exercise_id=e1.id, reps=15, sets=4)
    we2 = WorkoutExercise(workout_id=w1.id, exercise_id=e4.id, duration_seconds=60, sets=3)
    we3 = WorkoutExercise(workout_id=w2.id, exercise_id=e2.id, duration_seconds=1800)
    we4 = WorkoutExercise(workout_id=w2.id, exercise_id=e3.id, reps=10, sets=5)

    db.session.add_all([we1, we2, we3, we4])
    db.session.commit()

    print("Database successfully seeded!")