import os
import sys
from pathlib import Path

# Add project to path
project_dir = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_dir))

# Set settings module (Django style)
os.environ.setdefault('AIRFLOW_SETTINGS_MODULE', 'config.settings')

# Import and apply settings
from config.settings import AIRFLOW_CONFIG
from airflow.configuration import conf

# Configure Airflow
for section, options in AIRFLOW_CONFIG.items():
    for key, value in options.items():
        conf.set(section, key, str(value))

# WSGI app
from flask import Flask

app = Flask(__name__)

@app.route('/health')
def health():
    return {'status': 'healthy'}

application = app