from invoke import task


@task
def start_api(c):
    """Start the API server"""
    c.run("cd api && uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload")


@task
def migrate_database(c):
    """Run migrations"""
    c.run("cd database && alembic upgrade head")


@task
def reset_database(c):
    """Reset the database"""
    c.run("cd database && alembic downgrade base && alembic upgrade head")


@task
def update_data(c):
    """Update the data"""
    c.run("python3 etl/scripts/import_vehicle_updates.py")


@task
def run_dbt(c):
    """Run dbt"""
    c.run("cd etl/dldata_dbt && dbt run")


@task
def clean_dbt(c):
    """Clean dbt"""
    c.run("cd etl/dldata_dbt && dbt clean")
