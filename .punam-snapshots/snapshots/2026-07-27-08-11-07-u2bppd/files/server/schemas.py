from marshmallow import Schema, fields, validate, ValidationError

class ExerciseSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(
        required=True, 
        validate=validate.Length(min=2, error="Exercise name must be at least 2 characters long.")
    )
    category = fields.Str(
        required=True,
        validate=validate.OneOf(
            ['Cardio', 'Strength', 'Flexibility', 'Balance', 'Olympic'],
            error="Category must be one of: Cardio, Strength, Flexibility, Balance, Olympic"
        )
    )
    equipment_needed = fields.Bool(required=True)


class WorkoutExerciseSchema(Schema):
    id = fields.Int(dump_only=True)
    workout_id = fields.Int(dump_only=True)
    exercise_id = fields.Int(dump_only=True)
    reps = fields.Int(
        allow_none=True,
        validate=validate.Range(min=0, error="Reps must be 0 or greater.")
    )
    sets = fields.Int(
        allow_none=True,
        validate=validate.Range(min=0, error="Sets must be 0 or greater.")
    )
    duration_seconds = fields.Int(
        allow_none=True,
        validate=validate.Range(min=0, error="Duration seconds must be 0 or greater.")
    )
    exercise = fields.Nested(ExerciseSchema, dump_only=True)


class WorkoutSchema(Schema):
    id = fields.Int(dump_only=True)
    date = fields.Date(required=True, error_messages={"invalid": "Not a valid date. Format: YYYY-MM-DD"})
    duration_minutes = fields.Int(
        required=True,
        validate=validate.Range(min=1, error="Duration must be at least 1 minute.")
    )
    notes = fields.Str(allow_none=True)
    
    # Nested Serialization (Includes sets/reps/duration for stretch goal)
    workout_exercises = fields.Nested(WorkoutExerciseSchema, many=True, dump_only=True)


# Schema Instances
exercise_schema = ExerciseSchema()
exercises_schema = ExerciseSchema(many=True)

workout_schema = WorkoutSchema()
workouts_schema = WorkoutSchema(many=True)

workout_exercise_schema = WorkoutExerciseSchema()