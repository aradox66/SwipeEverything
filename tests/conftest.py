import pytest

from app import create_app, db
from app.models import Category, Preference, Thing, User
from config import Config


class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///test.db'
    WTF_CSRF_ENABLED = False
    BCRYPT_LOG_ROUNDS = 4


def fill_database():
    u0 = User(username='testuser', firstname='Austin', lastname='Tester')
    u0.set_password('userpw')
    u3 = User(username='testuser2', firstname='Lacy', lastname='Amil')
    u4 = User(username='testuser3', firstname='Sal', lastname='Andre')
    u5 = User(username='testuser4', firstname='Josh', lastname='Lago')
    u6 = User(username='testuser5', firstname='Holly', lastname='Ber')

    users = [u3, u4, u5, u6]

    things = []

    return users, things


@pytest.fixture(scope='class')
def test_client():
    flask_app = create_app(TestConfig)
    with flask_app.test_client() as client:
        app_context = flask_app.app_context()
        app_context.push()
        db.create_all()
        users, things = fill_database()
        for u in users:
            db.session.add(u)
        db.session.commit()
        for t in things:
            db.session.add(t)
        db.session.commit()
        yield client
        db.drop_all()
    app_context.pop()


@pytest.fixture(scope='class')
def auth_client(test_client):
    test_client.post('/login',
                     data=dict(username='testuser', password='userpw'),
                     follow_redirects=True)
    yield test_client
    test_client.get('/logout', follow_redirects=True)


@pytest.fixture(scope='function')
def logged_in_fxn(request, test_client):
    test_client.post('/login',
                     data=dict(username='testuser', password='userpw'),
                     follow_redirects=True)
    yield test_client

    def logout():
        test_client.get('/logout', follow_redirects=True)

    request.addfinalizer(logout)
