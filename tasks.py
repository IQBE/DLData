from invoke import task

@task
def start_api(c):
    """Start the API server"""
    c.run("cd api && uvicorn app.main:app --host 0.0.0.0 --port 8000")
  
@task
def migrate_database(c):
    """Run migrations"""
    c.run("cd database && alembic upgrade head")
    
@task
def reset_database(c):
    """Reset the database"""
    c.run("cd database && alembic downgrade base && alembic upgrade head")