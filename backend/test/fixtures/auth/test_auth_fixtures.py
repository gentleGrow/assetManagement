import pytest

from app.module.auth.model import User


@pytest.fixture
def user_instance() -> User:
    return User(id=1, social_id="google_social_id", provider="GOOGLE")
