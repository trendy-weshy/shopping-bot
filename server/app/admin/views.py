
from flask import url_for, redirect, request, abort
from flask_security import current_user, utils
from flask_admin.contrib.mongoengine import ModelView
from datetime import datetime


# SUPERUSER VIEW
class RolesView(ModelView):

    def is_accessible(self):
        if not current_user.is_active or not current_user.is_authenticated:
            return False

        if current_user.has_role('superuser'):
            return True

        return False

    def _handle_view(self, name, **kwargs):
        """
        Override builtin _handle_view in order to redirect users when a view is not accessible.
        """
        if not self.is_accessible():
            if current_user.is_authenticated:
                # permission denied
                abort(403)
            else:
                # login
                return redirect(url_for('security.login', next=request.url))

    can_edit = False
    create_modal = True
    can_export = True
    form_excluded_columns = ['created_on']


class UsersView(ModelView):
    column_editable_list = ['first_name', 'last_name']
    can_view_details = True
    view_details_modal = True
    column_searchable_list = ['first_name', 'last_name']
    column_exclude_list = ['password']
    form_excluded_columns = ['confirmed_at', 'created_on', 'active']
    can_export = True
    page_size = 50

    def on_model_change(self, form, model, is_created):
        model.password = utils.hash_password(model.password)

        if is_created:
            model.registered_on = datetime.now()  

    def is_accessible(self):
        if not current_user.is_active or not current_user.is_authenticated:
            return False

        if current_user.has_role('superuser'):
            return True

        return False

    def _handle_view(self, name, **kwargs):
        """
        Override builtin _handle_view in order to redirect users when a view is not accessible.
        """
        if not self.is_accessible():
            if current_user.is_authenticated:
                # permission denied
                abort(403)
            else:
                # login
                return redirect(url_for('security.login', next=request.url))
