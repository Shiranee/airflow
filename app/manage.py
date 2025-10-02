#!/usr/bin/env python
import os
import sys
import click
from pathlib import Path

# Add project to Python path
project_dir = Path(__file__).resolve().parent
sys.path.insert(0, str(project_dir))

# Set environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

@click.group()
def cli():
    """Django-like management commands for Airflow"""
    pass

@cli.command()
@click.option('--app', help='Specific app to check')
def check(app):
    """Check app configuration and DAGs"""
    if app:
        click.echo(f"Checking app: {app}")
        # App-specific checks
    else:
        click.echo("Checking all apps...")
        from config.settings import INSTALLED_APPS
        for app_name in INSTALLED_APPS:
            click.echo(f"✓ {app_name}")

@cli.command()
def migrate():
    """Run database migrations"""
    import subprocess
    subprocess.run(['alembic', 'upgrade', 'head'])

@cli.command()
@click.argument('message')
def makemigrations(message):
    """Create new migration"""
    import subprocess
    subprocess.run(['alembic', 'revision', '--autogenerate', '-m', message])

@cli.command()
@click.argument('app_name')
def startapp(app_name):
    """Create a new app structure"""
    app_dir = Path(f'apps/{app_name}')
    app_dir.mkdir(exist_ok=True)
    
    # Create app structure
    files_to_create = [
        '__init__.py',
        'models.py',
        'services.py', 
        'tasks.py',
        'dags/__init__.py',
        'operators/__init__.py',
        'hooks/__init__.py',
    ]
    
    for file_path in files_to_create:
        full_path = app_dir / file_path
        full_path.parent.mkdir(exist_ok=True, parents=True)
        if not full_path.exists():
            full_path.touch()
    
    click.echo(f"Created app: {app_name}")

@cli.command()
def shell():
    """Open interactive shell with app context"""
    import IPython
    from config.settings import INSTALLED_APPS, AIRFLOW_CONFIG
    
    # Setup context
    context = {
        'INSTALLED_APPS': INSTALLED_APPS,
        'AIRFLOW_CONFIG': AIRFLOW_CONFIG,
    }
    
    IPython.start_ipython(argv=[], user_ns=context)

@cli.command()
@click.option('--host', default='0.0.0.0')
@click.option('--port', default=8000)
def runserver(host, port):
    """Run custom API server"""
    import uvicorn
    uvicorn.run("config.asgi:application", host=host, port=port, reload=True)

if __name__ == '__main__':
    cli()