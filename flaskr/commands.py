import click
from flask.cli import with_appcontext
from flaskr.user import create_superuser

@click.command("create-superuser")
@with_appcontext
def cli_create_superuser():
    """Create a superuser via CLI."""
    create_superuser()

def register_commands(app):
    app.cli.add_command(cli_create_superuser)
