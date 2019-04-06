from app import create_app, db
from app.models import Lecturer, Student, Project

app = create_app()

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'Lecturer': Lecturer, 'Student': Student,
             'Project': Project}