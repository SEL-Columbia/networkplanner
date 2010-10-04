'Tests for people controller'
# Import system modules
import re
import urlparse
import simplejson
# Import custom modules
from np import model
from np.model import meta
from np.config import parameter
from np.lib import store, helpers as h
from np.tests import *


# Define shortcuts
username = 'username'
password = 'password'
email = 'username@example.com'
email_sms = ''
nickname = u'nickname'


class TestPeopleController(TestController):

    def setUp(self):
        'Clear tables'
        # Logout
        self.app.get(url('person_logout_plain'))
        # Delete all people
        meta.Session.rollback()
        meta.Session.query(model.Person).delete()
        meta.Session.query(model.PersonCandidate).delete()
        meta.Session.commit()

    def test_index(self):
        'Assert that the index page shows how many accounts are on file'
        # Initialize
        url_test = url('person_index')
        # Make sure that we begin with 0 people
        self.assert_('0 people' in self.app.get(url_test))
        # Add person
        meta.Session.add(model.Person(username, model.hashString(password), nickname, email))
        meta.Session.commit()
        # Make sure that we now have 1 person
        self.assert_('1 people' in self.app.get(url_test))

    def test_registration(self):
        'Make sure that registration works'
        # Make sure the registration page appears properly
        self.assert_('Registration' in self.app.get(url('person_register')))
        # Register the person
        self.app.post(url('person_register_'), dict(nickname=nickname, username=username, password=password, email=email, email_sms=email_sms))
        # Make sure the personCandidate exists
        self.assertEqual(meta.Session.query(model.PersonCandidate).filter_by(username=username).count(), 1)
        # Confirm registration
        self.app.get(url('person_confirm', ticket=meta.Session.query(model.PersonCandidate.ticket).filter_by(username=username).first()[0]))
        # Make sure the person exists
        self.assertEqual(meta.Session.query(model.Person).filter_by(username=username).count(), 1)

    def test_reset(self):
        """
        Make sure that resetting the password works
        Trying to reset an email that does not exist should return an error
        Make sure that resetting the password does not immediately change the password
        Make sure that reset confirmation works
        """
        # Reset an unfamiliar email
        self.assertEqual(simplejson.dumps({'isOk': 0}), self.app.post(url('person_reset'), dict(email=email)).body)
        # Add person
        meta.Session.add(model.Person(username, model.hashString(password), nickname, email))
        meta.Session.commit()
        # Reset password
        self.assertEqual(simplejson.dumps({'isOk': 1}), self.app.post(url('person_reset'), dict(email=email)).body)
        # Make sure the candidate exists
        self.assertEqual(meta.Session.query(model.PersonCandidate).filter_by(username=username).count(), 1)
        # Activate candidate
        self.app.get(url('person_confirm', ticket=meta.Session.query(model.PersonCandidate.ticket).filter_by(username=username).first()[0]))
        # Make sure the password has changed
        self.assertEqual(meta.Session.query(model.Person).filter_by(password_hash=model.hashString(password)).count(), 0)

    def test_update(self):
        """
        Make sure that updating credentials works
        Make sure the update page only appears when the user is logged in
        Make sure the update form is filled with the user's credentials
        Make sure that update_ only works when the user is logged in
        Make sure that update confirmation works
        """
        # Assert that we are redirected to the login page if the person is not logged in
        response = self.app.get(url('person_update'))
        self.assertEqual(urlparse.urlparse(response.response.location).path, url('person_login', targetURL=h.encodeURL('/')))
        # Assert that we get rejected if we try to post without logging in
        self.assertEqual(simplejson.dumps({'isOk': 0}), self.app.post(url('person_update_')).body)
        # Add person
        meta.Session.add(model.Person(username, model.hashString(password), nickname, email, email_sms))
        meta.Session.commit()
        # Log in
        self.app.post(url('person_login_'), dict(username=username, password=password))
        # Assert that the update form is filled with the user's credentials
        responseBody = self.app.get(url('person_update')).body
        self.assert_(username in responseBody)
        self.assert_(nickname in responseBody)
        self.assert_(email in responseBody)
        self.assert_(email_sms in responseBody)
        # Update credentials
        newUsername = store.makeRandomString(16)
        newPassword = store.makeRandomAlphaNumericString(parameter.PASSWORD_LENGTH_AVERAGE)
        newNickname = unicode(store.makeRandomString(16))
        newEmail = re.sub(r'.*@', store.makeRandomString(16) + '@', email)
        newEmailSMS = re.sub(r'.*@', store.makeRandomString(16) + '@', email)
        self.assertEqual(simplejson.dumps({'isOk': 1}), self.app.post(url('person_update_'), dict(username=newUsername, password=newPassword, nickname=newNickname, email=newEmail, email_sms=newEmailSMS)).body)
        # Make sure the credentials have not changed yet
        self.assertEqual(meta.Session.query(model.Person).filter_by(username=newUsername, password_hash=model.hashString(newPassword), nickname=newNickname, email=newEmail, email_sms=newEmailSMS).count(), 0)
        # Activate candidate
        self.app.get(url('person_confirm', ticket=meta.Session.query(model.PersonCandidate.ticket).filter_by(username=newUsername).first()[0]))
        # Make sure the credentials have changed
        self.assertEqual(meta.Session.query(model.Person).filter_by(username=newUsername, password_hash=model.hashString(newPassword), nickname=newNickname, email=newEmail, email_sms=newEmailSMS).count(), 1)

    def test_login(self):
        """
        Make sure that logging in works
        Ensure that the login page shows
        Ensure that bad credentials result in an error message
        Ensure that good credentials result in a proper redirect
        """
        # Initialize
        url_test = url('person_update')
        # Assert that the login page shows and stores url
        self.assert_('Login' in self.app.get(url('person_login', targetURL=h.encodeURL(url_test))))
        # Add person
        meta.Session.add(model.Person(username, model.hashString(password), nickname, email))
        meta.Session.commit()
        # Log in using bad credentials
        self.assertEqual(simplejson.dumps({'rejection_count': 1, 'isOk': 0}), self.app.post(url('person_login_'), dict(username=username, password=password + 'x')).body)
        # Log in using good credentials
        self.assertEqual(simplejson.dumps({'isOk': 1}), self.app.post(url('person_login_'), dict(username=username, password=password)).body)

    def test_logout(self):
        """
        Make sure that logging out works
        If the person is logged in, make sure the person gets logged out
        and is redirected properly.  If the person is already logged out, 
        return the user to the page before the user tried to log out.
        """
        # Initialize
        url_test = url('person_index')
        # Add person
        meta.Session.add(model.Person(username, model.hashString(password), nickname, email))
        meta.Session.commit()
        # Logging out should redirect back
        self.assert_(url_test in self.app.get(url('person_logout', targetURL=h.encodeURL(url_test))))
        # Log in
        self.assert_('Login' in self.app.get(url('person_login', targetURL=h.encodeURL(url_test))))
        self.assertEqual(simplejson.dumps({'isOk': 1}), self.app.post(url('person_login_'), dict(username=username, password=password)).body)
        # Logging out should redirect back
        self.assert_(url_test in self.app.get(url('person_logout', targetURL=h.encodeURL(url_test))))
