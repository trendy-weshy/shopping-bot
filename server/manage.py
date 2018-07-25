from mongoengine import DoesNotExist, NotUniqueError
from app.admin.models import Role, User
from app import create_app, db

application = create_app()

@application.shell_context_processor
def make_shell_context():
    return dict(app=application, db=db)


@application.cli.command('create_superuser')
def create_superuser():
    try:
        (
            User.objects.get(email='waweruj00@gmail.com')
        )
        print("superuser already exist")
    except DoesNotExist:
        new_user = User(
            email='waweruj00@gmail.com',
            password='john.8242',
            first_name='John',
            last_name='Wambugu'
        )
        new_user.save()


@application.cli.command('create_superuser_role')
def create_superuser_role():
    try:
        superuser = User.objects.get(email='waweruj00@gmail.com')
        role = Role(
            name='superuser',
            description='admin of all admins'
        )
        role.save()
        superuser.update(push__roles=role)
    except DoesNotExist:
        print("superuser account must exist in order to create a super admin role")
    except NotUniqueError:
        print("a superuser role already exist")