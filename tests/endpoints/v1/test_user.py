from fastapi.testclient import TestClient
from main import app
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import StaticPool
from core.models.database import get_db, Base
from core.models.user import User
from fastapi import Depends


SQLALCHEMY_DATBASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATBASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)


def overwrite_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = overwrite_get_db


client = TestClient(app)


def test_sign_up():
    response = client.post("/user", json={"username": "username", "password": "12345678"})
    assert response.status_code == 200
    assert response.json() == {"msg": "success"}


def test_sign_up_existed_user():
    response = client.post("/user", json={"username": "username2", "password": "12345678"})
    assert response.status_code == 200
    assert response.json() == {"msg": "success"}

    response = client.post("/user", json={"username": "username2", "password": "12345678"})
    assert response.status_code == 400
    assert response.json() == { "detail": "Username already registered"}


def test_invalid_user_name():
    invalid_user_names = [
        {
            "name": "n",
            "msg": "User name must be at least 2 characters long"
        },
        {
            "name": "a"*65,
            "msg": "User name must be shorter than 65 characters"
        },
        {
            "name": "username!",
            "msg": "User name cannot contains special characters"
        },
    ]
    for invalid_user_name in invalid_user_names:
        response = client.post("/user", json={"username": invalid_user_name["name"], "password": "super_safe_password"})
        assert response.status_code == 400
        assert response.json() == {"detail": invalid_user_name["msg"]}


def test_login():
    pass
