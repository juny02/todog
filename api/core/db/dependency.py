import os

from sqlmodel import Session, SQLModel, create_engine

HOST = os.getenv("DB_HOST", None)
PORT = os.getenv("DB_PORT", None)
DBNAME = os.getenv("DB_NAME", None)
USERNAME = os.getenv("DB_USERNAME", None)
PASSWORD = os.getenv("DB_PASSWORD", None)

POOL_SIZE = int(os.getenv("DB_POOL_SIZE", "5"))
MAX_OVERFLOW = int(os.getenv("DB_MAX_OVERFLOW", "10"))
DATABASE_URL = f"mysql+pymysql://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/{DBNAME}"

engine = create_engine(DATABASE_URL, connect_args={}, pool_size=POOL_SIZE, max_overflow=MAX_OVERFLOW)

### Use Alembic for database migrations instead of SQLModel's `create_all`
# SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session
