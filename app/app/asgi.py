import os
import sys
from pathlib import Path

# Add the project directory to Python path
project_dir = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_dir))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

# ASGI application for async operations
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Airflow Custom API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "airflow-async"}

@app.get("/api/v1/dag-stats")
async def get_dag_stats():
    # Custom async endpoint for DAG statistics
    from airflow.models import DagRun
    from airflow.utils.db import provide_session
    
    @provide_session
    def get_stats(session):
        # Your async logic here
        return {"total_runs": session.query(DagRun).count()}
    
    return get_stats()

application = app