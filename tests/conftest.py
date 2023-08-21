import pytest

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from core.models.database import Base


@pytest.fixture(scope="session")
def db():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(bind=engine)
    Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    session = Session()
    yield session
    session.close()


