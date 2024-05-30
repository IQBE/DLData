import os
from logging.config import fileConfig
from sqlalchemy import engine_from_config
from sqlalchemy import pool
from alembic import context

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = None

dbuser = os.getenv("DATABASE_USER", "unknown_user")
dbpassword = os.getenv("DATABASE_PASSWORD", "unknown_password")
dbhost = os.getenv("DATABASE_HOST", "unknown_host")
dbport = os.getenv("DATABASE_PORT", "unknown_port")
dbname = os.getenv("DATABASE_NAME", "unknown_name")

if any([
    dbhost == "unknown_host",
    dbuser == "unknown_user",
    dbport == "unknown_port",
    dbname == "unknown_name",
    dbpassword == "unknown_password",
]):
    unknown_variables = [var for var in [dbhost, dbuser, dbport, dbname, dbpassword] if var.startswith("unknown")]
    raise ValueError(f"Missing environment variables: {', '.join(unknown_variables)}.")

sqlalchemy_url = f"postgresql+psycopg://{dbuser}:{dbpassword}@{dbhost}:{dbport}/{dbname}"

config.set_main_option("sqlalchemy.url", sqlalchemy_url)


def run_migrations_offline() -> None:
    url = config.get_main_option("sqlalchemy.url")

    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
