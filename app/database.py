import logging
from sqlmodel import SQLModel, Session, create_engine
from app.config import get_settings
from contextlib import contextmanager

from app.utilities.security import encrypt_password

logger = logging.getLogger(__name__)

engine = create_engine(
    get_settings().database_uri, 
    echo=get_settings().env.lower() in ["dev", "development", "test", "testing", "staging"],
    pool_size=get_settings().db_pool_size,
    max_overflow=get_settings().db_additional_overflow,
    pool_timeout=get_settings().db_pool_timeout,
    pool_recycle=get_settings().db_pool_recycle,
)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def drop_all():
    SQLModel.metadata.drop_all(bind=engine)
    
def _session_generator():
    with Session(engine) as session:
        try:
            yield session
        except Exception as e:
            logger.error(f"Database session error: {e}")
            raise
        finally:
            session.close()

def get_session():
    yield from _session_generator()
    
def create_default_users():
    from app.models.user import Admin, User
    from sqlmodel import select
    with Session(engine) as session:
        if not session.exec(select(User)).first():
            password = encrypt_password("bobpass")
            regular_user = User(username="bob", password=password)
            session.add(regular_user)
            session.commit()
            logger.info("Default regular user created.")
        if not session.exec(select(Admin)).first():
            password = encrypt_password("freeyourmind")
            admin_user = Admin(username="morpheus", password=password)
            session.add(admin_user)
            session.commit()
            logger.info("Default admin user created.")

@contextmanager
def get_cli_session():
    yield from _session_generator()
