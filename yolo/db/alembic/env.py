import os
from logging.config import fileConfig
from sqlalchemy import create_engine
from alembic import context
from yolo.db.models import SQLModel

target_metadata = SQLModel.metadata
config = context.config
if config.config_file_name is not None:
    fileConfig(config.config_file_name)


def get_url():
    return os.getenv("YOLO_DATABASE_URL")


def run_migrations_offline():
    """Run migrations in 'offline' mode."""
    url = get_url()
    context.configure(url=url, target_metadata=target_metadata, literal_binds=True)

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Run migrations in 'online' mode."""
    connectable = create_engine(get_url())

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
