
import datetime
from flask_security import UserMixin, RoleMixin
from .. import db


class Role(db.Document, RoleMixin):
    name = db.StringField(unique=True)
    description = db.StringField()
    created_on = db.DateTimeField(default=datetime.datetime.now)

    def __str__(self):
        return self.name


class User(db.Document, UserMixin):
    first_name = db.StringField(required=True)
    last_name = db.StringField(required=True, unique_with='first_name')
    email = db.EmailField(required=True, unique=True)
    password = db.StringField(required=True, unique=True)
    active = db.BooleanField(default=True)
    confirmed_at = db.DateTimeField(required=False)
    created_on = db.DateTimeField(default=datetime.datetime.now)
    roles = db.ListField(db.ReferenceField(Role), default=[])

    def __str__(self):
        return self.first_name, self.last_name, self.email

