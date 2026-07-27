# Workout Tracker API

A RESTful Flask API for managing workout sessions, exercises, and their relationships. Built with Flask, Flask-SQLAlchemy, Flask-Migrate, and Marshmallow for database ORM and serialization.

---

##  Project Structure

```text
workout-tracker-api/
├── Pipfile
├── Pipfile.lock
├── README.md
└── server/
    ├── app.py          # Application entry point and API route definitions
    ├── config.py       # Flask app setup and database configuration
    ├── models.py       # SQLAlchemy database models
    ├── schemas.py      # Marshmallow serialization/validation schemas
    ├── seed.py         # Database seed script
    └── migrations/     # Alembic database migration files
Tech StackPython 3.12 / 3.8+Flask (2.2.2)Flask-SQLAlchemy (3.0.3) & SQLAlchemyFlask-Migrate (3.1.0) & AlembicMarshmallow (3.20.1)SQLiteSetup & Installation1. Clone the RepositoryBashgit clone [https://github.com/YOUR_GITHUB_USERNAME/workout-tracker-api.git](https://github.com/YOUR_GITHUB_USERNAME/workout-tracker-api.git)
cd workout-tracker-api
2. Activate Virtual Environment & Install DependenciesUsing pipenv:Bashpipenv install --skip-lock
pipenv shell
Or using venv:Bashpython3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt  # or install via pipenv
Database Setup & SeedingNavigate into the server/ directory and execute migrations:Bashcd server

# Initialize and apply migrations
flask db init
flask db migrate -m "Initial migration"
flask db upgrade

# Populate database with sample data
python3 seed.py
Running the ApplicationFrom inside the server/ directory with your virtual environment activated:Bashpython3 app.py
The server will start running locally at: http://127.0.0.1:5555🛠️ API EndpointsGeneralMethodEndpointDescriptionGET/Welcome messageWorkoutsMethodEndpointDescriptionGET/workoutsRetrieve all workoutsGET/workouts/<id>Retrieve a specific workout by IDPOST/workoutsCreate a new workoutPATCH/workouts/<id>Update an existing workoutDELETE/workouts/<id>Delete a workoutExercisesMethodEndpointDescriptionGET/exercisesRetrieve all exercisesGET/exercises/<id>Retrieve a specific exercise by IDPOST/exercisesCreate a new exerciseDELETE/exercises/<id>Delete an exerciseWorkout Exercises (Join Table)MethodEndpointDescriptionPOST/workout_exercisesAssociate an exercise with a workout