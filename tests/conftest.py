import pytest
from app import create_app,Members

@pytest.fixture()
def app():
    app = create_app("testing")
    app.config.update({
        "TESTING": True,
    })
    return app

@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def runner(app):
    return app.test_cli_runner()

@pytest.fixture()
def create_member():
    member=Members(name="demouser",email="demo@123")
    return member
