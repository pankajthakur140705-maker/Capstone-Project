from logging.config import fileConfig
import sys
import os

from sqlalchemy import engine_from_config, pool
from alembic import context

# ---------------------------
# Alembic Config
# ---------------------------
config = context.config

# Logging setup
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# ---------------------------
# ADD PROJECT ROOT TO PATH
# ---------------------------
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(BASE_DIR)

# ---------------------------
# IMPORT BASE + MODELS
# ---------------------------
from app.database.db import Base
from app.models import scheme_model  # ensures table is registered

target_metadata = Base.metadata


# ---------------------------
# MIGRATION: OFFLINE
# ---------------------------
def run_migrations_offline() -> None:
    url = config.get_main_option("sqlalchemy.url")

    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True,
        compare_server_default=True,
    )

    with context.begin_transaction():
        context.run_migrations()


# ---------------------------
# MIGRATION: ONLINE
# ---------------------------
def run_migrations_online() -> None:
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:

        context.configure(
            connection=connection,
            target_metadata=target_metadata,

            # IMPORTANT FIXES FOR SQLITE + SCHEMA CHANGES
            compare_type=True,
            compare_server_default=True,
            render_as_batch=True,   # REQUIRED for SQLite ALTER TABLE support
        )

        with context.begin_transaction():
            context.run_migrations()


# ---------------------------
# RUN
# ---------------------------
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()