import pytest
from flask import url_for
from flask_login import current_user

from app import db
from app.models import User


@pytest.mark.usefixtures('test_client')
class TestFixtures():
    def test_login_fail(self, test_client):
        response = test_client.get('/', follow_redirects=True)
        assert b'Sign in' in response.data


@pytest.mark.usefixtures('auth_client')
class TestProfile():
    def test_access_profile(self, auth_client):
        """Logged-in user is able to access their profile page."""
        response = auth_client.get(url_for('swipes.home'),
                                   follow_redirects=True)
        assert b'Swipe Everything' in response.data
