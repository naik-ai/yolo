from sqlmodel import SQLModel
from alembic import context
from sqlalchemy import engine_from_config, pool
from logging.config import fileConfig

# from yolo.db.models import (
#     User,
#     IPLSchedule,
#     PlayerStats,
#     MatchStats,
#     MatchPoll,
#     PollResults,
#     GamePitchAnalysis,
# )

config = context.config
fileConfig(config.config_file_name)
target_metadata = SQLModel.metadata


def run_migrations_offline():
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()


if __name__ == "__main__":

    if context.is_offline_mode():
        run_migrations_offline()
    else:
        run_migrations_online()
