from logging.config import fileConfig

from sqlalchemy import create_engine, engine_from_config
from sqlalchemy import pool

import os
from alembic import context
from api.model import db
from api.model import character, classes, dice, items, spellbook, spells, user


# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
target_metadata = db.Model.metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.

DATABASE_URL = os.environ.get('DATABASE_URL')
if DATABASE_URL is None:
    print('Could not get environment variable for DATABASE_URL. Using default in alembic.ini.')
    DATABASE_URL = config.get_main_option("sqlalchemy.url")

print(f"Using database url: {DATABASE_URL}")

def run_offline_migrations() -> None:
    context.configure(
        url=DATABASE_URL,
        target_metadata=target_metadata,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()

def run_migrations() -> None:
    connectable = create_engine(DATABASE_URL)

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_offline_migrations()
else:
    run_migrations()
