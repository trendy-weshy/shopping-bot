import flask_admin
from flask import url_for
from flask_admin import helpers as admin_helpers
from flask_security import Security, MongoEngineUserDatastore

from . import views, models
from .. import db


def create_admin_console(app):
    # Admin Panel

    user_datastore = MongoEngineUserDatastore(db, models.User, models.Role)
    security = Security(app, user_datastore)

    admin_console = flask_admin.Admin(
        app,
        'Jumiabot System Dashboard',
        base_template='my_master.html',
        template_mode='bootstrap3',
    )

    admin_console.add_view(views.RolesView(models.Role))
    admin_console.add_view(views.UsersView(models.User))

    @security.context_processor
    def security_context_processor():
        return dict(
            admin_base_template=admin_console.base_template,
            admin_view=admin_console.index_view,
            h=admin_helpers,
            get_url=url_for
        )

