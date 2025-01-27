import time
from sqlalchemy import create_engine, MetaData, inspect, text
from sqlalchemy.orm import declarative_base, sessionmaker, configure_mappers
from enum import Enum
import sqlalchemy as sa
from sqlalchemy.exc import OperationalError
from libs.shared.config.settings import Stage, settings

# Import the centralized settings


# Define the base model class with schema handling
if settings.STAGE == Stage.LOCAL:
    Base = declarative_base(
        type_annotation_map={Enum: sa.Enum(Enum, inherit_schema=True)}
    )
else:
    metadata = MetaData(schema=settings.POSTGRES_SCHEMA)
    Base = declarative_base(
        metadata=metadata,
        type_annotation_map={Enum: sa.Enum(Enum, inherit_schema=True)},
    )


# Create SQLAlchemy engines
write_engine = create_engine(settings.POSTGRES_WRITE_URL)
read_engine = create_engine(settings.POSTGRES_READ_URL)

# Function to create schema if needed
def create_schema_if_not_exists(engine):
    inspector = inspect(engine)
    if settings.POSTGRES_SCHEMA not in inspector.get_schema_names():
        with engine.connect() as conn:
            conn.execute(text(f"CREATE SCHEMA IF NOT EXISTS {settings.POSTGRES_SCHEMA}"))
            conn.commit()

# Retry logic with settings-based schema
def wait_for_db(engine, retries=10, delay=10):
    for i in range(retries):
        try:
            create_schema_if_not_exists(engine)
            break
        except OperationalError:
            if i < retries - 1:
                print(f"Database not ready. Retrying in {delay}s...")
                time.sleep(delay)
            else:
                print("Max retries reached. Database unavailable.")
                raise

# Initialize database connections
wait_for_db(write_engine)
wait_for_db(read_engine)

# Configure SQLAlchemy mappings
configure_mappers()

# Session factories with updated variable names
WriteSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=write_engine)
ReadSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=read_engine)

def get_db():
    """Yield write session"""
    db = WriteSessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_db_ro():
    """Yield read-only session"""
    db = ReadSessionLocal()
    try:
        yield db
    finally:
        db.close()