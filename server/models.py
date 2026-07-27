from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
from sqlalchemy import CheckConstraint
import re

db = SQLAlchemy()


class Exercise(db.Model):
    __tablename__ = 'exercises'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)  # Constraint 1
    category = db.Column(db.String, nullable=False)           # Constraint 2
    equipment_needed = db.Column(db.Boolean, nullable=False, default=False)

    # Relationships
    workout_exercises = db.relationship(
        'WorkoutExercise', 
        back_populates='exercise', 
        cascade='all, delete-orphan'
    )
    workouts = db.relationship(
        'Workout', 
        secondary='workout_exercises', 
        back_populates='exercises'
    )

    # Model Validations
    @validates('name')
    def validate_name(self, key, name):
        if not name or not name.strip():
            raise ValueError("Exercise name cannot be empty.")
        if len(name.strip()) < 2:
            raise ValueError("Exercise name must be at least 2 characters long.")
        return name.strip()

    @validates('category')
    def validate_category(self, key, category):
        valid_categories = ['Cardio', 'Strength', 'Flexibility', 'Balance', 'Olympic']
        if category not in valid_categories:
            raise ValueError(f"Category must be one of: {', '.join(valid_categories)}")
        return category

    def __repr__(self):
        return f"<Exercise {self.id}: {self.name} ({self.category})>"


class Workout(db.Model):
    __tablename__ = 'workouts'

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)                  # Constraint 3
    duration_minutes = db.Column(db.Integer, nullable=False)  # Constraint 4
    notes = db.Column(db.Text, nullable=True)

    __table_args__ = (
        CheckConstraint('duration_minutes > 0', name='check_duration_positive'),  # Check Constraint
    )

    # Relationships
    workout_exercises = db.relationship(
        'WorkoutExercise', 
        back_populates='workout', 
        cascade='all, delete-orphan'
    )
    exercises = db.relationship(
        'Exercise', 
        secondary='workout_exercises', 
        back_populates='workouts'
    )

    # Model Validation
    @validates('duration_minutes')
    def validate_duration(self, key, duration):
        if duration is None or duration <= 0:
            raise ValueError("Duration must be a positive integer greater than zero.")
        return duration

    def __repr__(self):
        return f"<Workout {self.id}: {self.date} ({self.duration_minutes} mins)>"


class WorkoutExercise(db.Model):
    __tablename__ = 'workout_exercises'

    id = db.Column(db.Integer, primary_key=True)
    workout_id = db.Column(db.Integer, db.ForeignKey('workouts.id'), nullable=False)
    exercise_id = db.Column(db.Integer, db.ForeignKey('exercises.id'), nullable=False)
    reps = db.Column(db.Integer, nullable=True)
    sets = db.Column(db.Integer, nullable=True)
    duration_seconds = db.Column(db.Integer, nullable=True)

    __table_args__ = (
        CheckConstraint('reps IS NULL OR reps >= 0', name='check_reps_non_negative'),
        CheckConstraint('sets IS NULL OR sets >= 0', name='check_sets_non_negative'),
        CheckConstraint('duration_seconds IS NULL OR duration_seconds >= 0', name='check_duration_sec_non_negative'),
    )

    # Relationships
    workout = db.relationship('Workout', back_populates='workout_exercises')
    exercise = db.relationship('Exercise', back_populates='workout_exercises')

    # Model Validation
    @validates('reps', 'sets', 'duration_seconds')
    def validate_metrics(self, key, value):
        if value is not None and value < 0:
            raise ValueError(f"{key.replace('_', ' ').capitalize()} cannot be negative.")
        return value

    def __repr__(self):
        return f"<WorkoutExercise W:{self.workout_id} E:{self.exercise_id}>"