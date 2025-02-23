import os
from logging.config import fileConfig

from alembic import context
from sqlalchemy import engine_from_config, pool

from app.dog_family.adapter.output.persistence.entities.DogFamilySQLModelEntity import DogFamilySQLModelEntity
from app.user.adapter.output.persistence.entities.UserSQLModelEntity import UserSQLModelEntity
from app.dog.adapter.output.persistence.entities.DogSQLModelEntity import DogSQLModelEntity
from app.treat.adapter.output.persistence.entities.TreatSQLModelEntity import TreatSQLModelEntity
from app.treat_record.adapter.output.persistence.entities.TreatRecordSQLModelEntity import TreatRecordSQLModelEntity
from app.walk_record.adapter.output.persistence.entities.WalkRecordSQLModelEntity import WalkRecordSQLModelEntity
from app.meal_record.adapter.output.persistence.entities.MealRecordSQLModelEntity import MealRecordSQLModelEntity
from app.memo.adapter.output.persistence.entities.MemoSQLModelEntity import MemoSQLModelEntity


from sqlmodel import SQLModel

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)


username = os.getenv("DB_USERNAME")
password = os.getenv("DB_PASSWORD")
host = os.getenv("DB_HOST")
port = os.getenv("DB_PORT")
db_name = os.getenv("DB_NAME")
url = f"mysql+pymysql://{username}:{password}@{host}:{port}/{db_name}"
config.set_main_option("sqlalchemy.url", url)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
target_metadata = SQLModel.metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
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
