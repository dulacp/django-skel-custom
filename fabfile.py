"""Management utilities."""


from fabric.contrib.console import confirm
from fabric.api import abort, env, local, settings, task


########## GLOBALS
env.run = 'heroku run python manage.py'
HEROKU_ADDONS = (
    'cloudamqp:lemur',
    'heroku-postgresql:dev',
    'scheduler:standard',
    'memcachier:dev',
    'newrelic:standard',
    'pgbackups:auto-month',
    'sentry:developer',
)
HEROKU_CONFIGS = (
    'DJANGO_SETTINGS_MODULE={{ project_name }}.settings.prod',
    'SECRET_KEY="{{ secret_key }}"'
    'AWS_ACCESS_KEY_ID=xxx',
    'AWS_SECRET_ACCESS_KEY=xxx',
    'AWS_STORAGE_BUCKET_NAME=xxx',
)
########## END GLOBALS


########## HELPERS
def cont(cmd, message):
    """Given a command, ``cmd``, and a message, ``message``, allow a user to
    either continue or break execution if errors occur while executing ``cmd``.

    :param str cmd: The command to execute on the local system.
    :param str message: The message to display to the user on failure.

    .. note::
        ``message`` should be phrased in the form of a question, as if ``cmd``'s
        execution fails, we'll ask the user to press 'y' or 'n' to continue or
        cancel exeuction, respectively.

    Usage::

        cont('heroku run ...', "Couldn't complete %s. Continue anyway?" % cmd)
    """
    with settings(warn_only=True):
        result = local(cmd, capture=True)

    if message and result.failed and not confirm(message):
        abort('Stopped execution per user request.')
########## END HELPERS


########## DATABASE MANAGEMENT
@task
def syncdb():
    """Run a syncdb."""
    local('%(run)s syncdb --noinput' % env)


@task
def migrate(app=None):
    """Apply one (or more) migrations. If no app is specified, fabric will
    attempt to run a site-wide migration.

    :param str app: Django app name to migrate.
    """
    if app:
        local('%s migrate %s --noinput' % (env.run, app))
    else:
        local('%(run)s migrate --noinput' % env)
########## END DATABASE MANAGEMENT


########## FILE MANAGEMENT
@task
def collectstatic():
    """Collect all static files, and copy them to S3 for production usage."""
    local('%(run)s collectstatic --noinput' % env)
########## END FILE MANAGEMENT


########## HEROKU MANAGEMENT
@task
def bootstrap():
    """Bootstrap your new application with Heroku, preparing it for a production
    deployment. This will:

        - Create a new Heroku application.
        - Install all ``HEROKU_ADDONS``.
        - Sync the database.
        - Apply all database migrations.
        - Initialize New Relic's monitoring add-on.
    """
    cont('heroku create', "Couldn't create the Heroku app, continue anyway?")

    for addon in HEROKU_ADDONS:
        cont('heroku addons:add %s' % addon,
            "Couldn't add %s to your Heroku app, continue anyway?" % addon)

    for config in HEROKU_CONFIGS:
        cont('heroku config:add %s' % config,
            "Couldn't add %s to your Heroku app, continue anyway?" % config)

    cont('git push heroku master',
            "Couldn't push your application to Heroku, continue anyway?")

    syncdb()
    migrate()

    cont('%(run)s newrelic-admin validate-config - stdout' % env,
            "Couldn't initialize New Relic, continue anyway?")


@task
def destroy():
    """Destroy this Heroku application. Wipe it from existance.

    .. note::
        This really will completely destroy your application. Think twice.
    """
    local('heroku apps:destroy')
########## END HEROKU MANAGEMENT


########## PROJECT MANAGEMENT
import os

local_env = 'python manage.py'
PROJECT_DIR = '{{ project_name }}'
APP_SUB_DIRECTORY = os.path.join(PROJECT_DIR, 'apps')

# templates
TEMPLATE_APP_DIRECTORY = '/Users/peteralaoui/Sites/_CodeTemplates/django_app_template'
TEMPLATE_COMMAND_FILE = '/Users/peteralaoui/Sites/_CodeTemplates/django_command_template.py'

@task
def startapp(app_name):
    """Create an app with my personnal template :)"""
    app_directory = os.path.join(APP_SUB_DIRECTORY, app_name)
    if not os.path.exists(app_directory):
        os.makedirs(app_directory)
    local('%s startapp --template %s %s %s' % (local_env, TEMPLATE_APP_DIRECTORY, app_name, app_directory))

    # create the template side directory
    template_files_directory = os.path.join(PROJECT_DIR, 'templates')
    app_template_files_directory = os.path.join(template_files_directory, app_name)
    if not os.path.exists(app_template_files_directory):
        os.makedirs(app_template_files_directory)
    index_template_path = os.path.join(app_template_files_directory, 'index.html')
    with open(index_template_path, 'w+') as index_template_file:
        index_template_file.write("<h1>Hello world</h1><p>from the '%s' app</p>" % app_name)

@task
def startcommand(app_name, command_name):
    """Prepare the command file"""
    app_directory = os.path.join(APP_SUB_DIRECTORY, app_name)
    if not os.path.exists(app_directory):
        abort("This app doesn't seem to exist or is not in the usuable path '%s'" % app_directory)

    commands_directory = os.path.join(app_directory, 'management/commands')
    if not os.path.exists(commands_directory):
        os.makedirs(commands_directory)

    empty_files = ['management/__init__.py', 'management/commands/__init__.py']
    for f in empty_files:
        local('touch %s' % os.path.join(app_directory, f))

    # create the command file
    command_path = os.path.join(commands_directory, '%s.py' % command_name)
    with open(command_path, 'w+') as command_file:
        template = open(TEMPLATE_COMMAND_FILE, 'r').read()
        context = {'app_name': app_name, 'command_name': command_name}
        template_rendered = template % context
        command_file.write(template_rendered)
########## END PROJECT MANAGEMENT


########## USER PROJECT MANAGEMENT
########## END USER PROJECT MANAGEMENT
