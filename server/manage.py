import os
from app import create_app, db
import click

application = create_app()

@application.shell_context_processor
def make_shell_context():
    return dict(app=application, db=db)
