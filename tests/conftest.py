import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.database import Base, get_db
from app.models import User
from app.auth import get_password_hash


SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create the database tables before tests run
Base.metadata.create_all(bind=engine)

@pytest.fixture(scope="function")
def db():
    """
    Fixture to provide a database session to a test function.
    This will also drop and recreate the tables for each test.
    """
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture(scope="function")
def client(db):
    """
    Fixture to provide a TestClient instance that uses the test database.
    """
    def override_get_db():
        try:
            db = TestingSessionLocal()
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    del app.dependency_overrides[get_db]


@pytest.fixture
def test_user(db):
    """Fixture to create a test user in the database."""
    user_data = {
        "email": "test@example.com",
        "password": "testpassword"
    }
    user = User(
        email=user_data["email"],
        hashed_password=get_password_hash(user_data["password"])
    )
    db.add(user)
    db.commit()
    return user_data

@pytest.fixture
def auth_token(client, test_user):
    """Fixture to get an authentication token for the test user."""
    response = client.post(
        "/api/v1/token",
        data={"username": test_user["email"], "password": test_user["password"]},
    )
    assert response.status_code == 200
    return response.json()["access_token"]