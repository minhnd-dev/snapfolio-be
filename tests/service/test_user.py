from core.models.user import User
from core.services.user import UserService, UserExistedError
from pytest import raises


def test_create_user(db):
    user_service = UserService(db)

    user_data = {
        "username": "testuser",
        "password": "abcxyzghijkl"
    }

    user = user_service.create_user(user_data["username"], user_data["password"])

    assert db.query(User).filter(User.username==user_data["username"]).first() == user


def test_create_user_existed(db):
    user_service = UserService(db)

    user_data = {
        "username": "testuserexisted",
        "password": "abcxyzghijkl"
    }


    user_service.create_user(user_data["username"], user_data["password"])

    with raises(UserExistedError): 
        user_service.create_user(user_data["username"], user_data["password"])

