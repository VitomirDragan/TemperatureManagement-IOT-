import os
import unittest
from flask_login import current_user
from Implementation import app
from flask_testing import TestCase
from Implementation import db, Users, bcrypt


class BaseTestCase(TestCase):
    def create_app(self):
        # Adapt app configuration for unit testing
        app.config['DEBUG'] = True
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['SECRET_KEY'] = str(os.environ.get("FLASK_SECRET_KEY"))
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        return app

    # This function sets the environment for testing and is called before each test
    def setUp(self):
        db.create_all()  # Create separate database for testing

        # Add users in database
        db.session.add(
            Users(id=1, username="userAdmin", password="$2y$12$hKqOLsmzYyNXneMe3JlK1ePP6pI03ZAMuCd6dRm8eiq.fO3R7xJxy",
                  admin_role=True))
        db.session.add(
            Users(id=2, username="userNotAdmin",
                  password="$2y$12$gAEZGDpw1uVqRmiXy5Fg1ur6ct5Lj/uVD3U/6iYBkdb6vCUjneyWG",
                  admin_role=False))
        db.session.add(
            Users(id=3, username="user",
                  password="$2y$12$79rHIau.YBofPRJmyw8nlOuFYlK6RHnkvCQL2jZfJ2POg4Z.hSeZ6",
                  admin_role=True))

        db.session.commit()  # Commit changes

    # This function restores the environment to default. It is called after each test
    def tearDown(self):
        db.session.remove()  # Delete SQLAlchemy session
        db.drop_all()  # Remove database


class CommonTestCase(BaseTestCase):
    def test_loginIsRequired_home(self):
        """Access home page url without logging in first. The application must return unauthorized html error"""
        resp = self.client.get('/home', follow_redirects=True)  # Access home page url
        self.assert_status(resp, 401,
                           'Security error! Home page can be accessed by users that are not logged in.')  # If the access is allowed, return a security error message

    def test_loginIsRequired_register(self):
        """Access register page url without logging in first. The application must return unauthorized html error"""
        resp = self.client.get('/register', follow_redirects=True)
        self.assert_status(resp, 401,
                           'Security error! Register page can be accessed by users that are not logged in.')  # If the access is allowed, return a security error message

    def test_loginIsRequired_viewAccounts(self):
        """Access viewAccounts page url without logging in first. The application must return unauthorized html error"""
        resp = self.client.get('/viewAccounts', follow_redirects=True)  # Access viewAccounts page url
        self.assert_status(resp, 401,
                           'Security error! View accounts page can be accessed by users that are not logged in.')  # If the access is allowed, return a security error message

    def test_loginIsRequired_delteAccount(self):
        """Access deleteAccount url without logging in first. The application must return unauthorized html error"""
        resp = self.client.get('/deleteAccount/1', follow_redirects=True)  # Access deleteAccount url
        self.assert_status(resp, 401,
                           'Security error! Accounts can be deleted by users which are not logged in.')  # If the access is allowed, return a security error message

    def test_loginIsRequired_giveAdminRights(self):
        """Access giveAdminRights url without logging in first. The application must return unauthorized html error"""
        resp = self.client.get('/giveAdminRights/1', follow_redirects=True)  # Access giveAdminRights url
        self.assert_status(resp, 401,
                           'Security error! An user which is not logged in can give admin rights to other accounts.')  # If the access is allowed, return a security error message

    def test_loginIsRequired_removeAdminRights(self):
        """Access removeAdminRights url without logging in first. The application must return unauthorized html error"""
        resp = self.client.get('/removeAdminRights/1', follow_redirects=True)  # Access removeAdminRights url
        self.assert_status(resp, 401,
                           'Security error! An user which is not logged in can remove admin rights from other accounts')  # If the access is allowed, return a security error message

    def test_loginIsRequired_changePassword(self):
        """Access changePassword page url without logging in first. The application must return unauthorized html error"""
        resp = self.client.get('/changePassword', follow_redirects=True)  # Access changePassword page url
        self.assert_status(resp, 401,
                           'Security error! Change password page can be accessed by users that are not logged in.')  # If the access is allowed, return a security error message

    def test_loginIsRequired_switchIntervalsOn(self):
        """Access switchIntervalsOn url without logging in first. The application must return unauthorized html error"""
        resp = self.client.get('/switchIntervalsOn', follow_redirects=True)  # Access switchIntervalsOn url
        self.assert_status(resp, 401,
                           'Security error! Intervals can be switched on or off by users which are not logged in.')  # If the access is allowed, return a security error message

    def test_loginIsRequired_setIntervalsForWorkingDays(self):
        """Access setIntervalsForWorkingDay url without logging in first. The application must return unauthorized html error"""
        resp = self.client.get('/setIntervalsForWorkingDays',
                               follow_redirects=True)  # Access setIntervalsForWorkingDay url
        self.assert_status(resp, 401,
                           'Security error! Intervals for working days can be set by users which are not logged in.')  # If the access is allowed, return a security error message

    def test_loginIsRequired_setIntervalsForWeekend(self):
        """Access setIntervalsForWeekend url without logging in first. The application must return unauthorized html error"""
        resp = self.client.get('/setIntervalsForWeekend', follow_redirects=True)  # Access setIntervalsForWeekend url
        self.assert_status(resp, 401,
                           'Security error! Intervals for weekend can be set by users which are not logged in.')  # If the access is allowed, return a security error message

    def test_loginIsRequired_logOut(self):
        """Access logOut url without logging in first. The application must return unauthorized html error"""
        resp = self.client.get('/logout', follow_redirects=True)  # Access logOut url
        self.assert_status(resp, 401,
                           'Security error! An user can logout without being logged in.')  # If the access is allowed, return a security error message

    def test_notExistentAccount(self):
        """If the username does not exist in database, the login should not succeed and an error message should be displayed"""
        with self.client:
            resp = self.client.post('/',
                                    data=dict(username='notPresentInDatabase', password='notPresentInDatabase'),
                                    follow_redirects=True
                                    )  # Try to connect with an account that does not exist in database
            self.assertIn(
                b'This account does not exist in our database! Please contact the administrator for creating one!',
                resp.data)  # Verify if the message is displayed
            self.assertFalse(current_user.is_authenticated)  # Test is passed if the user is not authenticated

    def test_passwordEncryption(self):
        """Verify that the password is encrypted"""
        with self.client:
            self.client.post(
                '/',
                data=dict(username="userAdmin", password="userAdmin"),
                follow_redirects=True
            )  # Connect to database with an existing account

            # Verify that the encrypted password is corresponding to the correct password
            self.assertTrue(bcrypt.check_password_hash(current_user.password, 'userAdmin'))
            self.assertFalse(bcrypt.check_password_hash(current_user.password, 'wrongPassword'))

    def test_login(self):
        """Verify that a user is logged in if introduces the correct credentials"""
        with self.client:
            resp = self.client.post('/',
                                    data=dict(username='userNotAdmin', password='userNotAdmin'),
                                    follow_redirects=True
                                    )  # Log in with correct credentials
            self.assertIn(b'Switch intervals on/off',
                          resp.data)  # Verify that the correct page is displayed after logging in
            self.assertTrue(current_user.username == 'userNotAdmin')
            self.assertTrue(current_user.is_authenticated)  # Verify that the user is logged in

    def test_incorrectLogin(self):
        """Verify if user that enters wrong password is not allowed to login and error message is displayed"""
        with self.client:
            resp = self.client.post('/',
                                    data=dict(username='userNotAdmin', password='incorrectPassword'),
                                    follow_redirects=True
                                    )  # Try to log in with wrong password
            self.assertIn(b'Username', resp.data)  # Verify that the user is redirected to login page
            self.assertIn(
                b'Wrong credentials!', resp.data)  # Verify if the message is displayed
            self.assertFalse(current_user.is_authenticated)  # Test is passed if the user is not authenticated

    def test_logOut(self):
        """Verify the log out functionality"""
        with self.client:
            self.client.post('/',
                             data=dict(username='userNotAdmin', password='userNotAdmin'),
                             follow_redirects=True
                             )  # Log in with a valid account
            resp = self.client.get('/logout', follow_redirects=True)  # Access the log out url
            self.assertIn(b'Username', resp.data)  # Verify that the user is redirected tp log in page
            self.assertFalse(current_user.is_authenticated)  # Test is passed if the user is not authenticated

    def test_switchIntervalsOn(self):
        """Verify that the functionality to change the operating mode of the system is available"""
        with self.client:
            self.client.post('/',
                             data=dict(username='userNotAdmin', password='userNotAdmin'),
                             follow_redirects=True
                             )  # Log in with a valid account
            resp = self.client.post('/switchIntervalsOn',
                                    data=dict(switchIntervalsOn='1'),
                                    follow_redirects=True)  # Turn the automatic mode on
            self.assertTrue(b'Schedule' in resp.data)  # Verify that the 'Schedule' button appeared

    def test_switchIntervalsOff(self):
        """Verify that the functionality to change the operating mode of the system is available"""
        with self.client:
            self.client.post('/',
                             data=dict(username='userNotAdmin', password='userNotAdmin'),
                             follow_redirects=True
                             )  # Log in with a valid account
            resp = self.client.post('/switchIntervalsOn',
                                    data=dict(switchIntervalsOn='0'),
                                    follow_redirects=True)  # Turn the manual mode on
            self.assertFalse(b'Schedule' in resp.data)  # Verify that the 'Schedule' button disappeared

    def test_setIntervalsWorkingDay(self):
        """Verify that the application allows user to set intervals for working days"""
        with self.client:
            self.client.post('/',
                             data=dict(username='userNotAdmin', password='userNotAdmin'),
                             follow_redirects=True
                             )  # Log in with a valid account
            self.client.post('/switchIntervalsOn',
                             data=dict(switchIntervalsOn='1'),
                             follow_redirects=True)  # Turn on the automatic mode
            resp = self.client.post('/setIntervalsForWorkingDays',
                                    data=dict(firstWorkingDayInterval='06:00',
                                              secondWorkingDayInterval='08:00',
                                              thirdWorkingDayInterval='16:00',
                                              fourthWorkingDayInterval='22:00',
                                              temperatureFirstWDInterval='22',
                                              temperatureSecondWDInterval='21',
                                              temperatureThirdWDInterval='22',
                                              temperatureFourthWDInterval='20'),
                                    follow_redirects=True)  # Set time intervals and temperatures
            self.assertIn(b'Intervals were set successfully!',
                          resp.data)  # Verify that the success message is displayed

    def test_setIntervalsWorkingDayNotChronologically(self):
        """Verify that time intervals are not stored in database if they are not set chronologically"""
        with self.client:
            self.client.post('/',
                             data=dict(username='userNotAdmin', password='userNotAdmin'),
                             follow_redirects=True
                             )  # Log in with a valid account
            self.client.post('/switchIntervalsOn',
                             data=dict(switchIntervalsOn='1'),
                             follow_redirects=True)  # Turn on the automatic mode
            resp = self.client.post('/setIntervalsForWorkingDays',
                                    data=dict(firstWorkingDayInterval='08:00',
                                              secondWorkingDayInterval='06:00',
                                              thirdWorkingDayInterval='22:00',
                                              fourthWorkingDayInterval='16:00',
                                              temperatureFirstWDInterval='22',
                                              temperatureSecondWDInterval='21',
                                              temperatureThirdWDInterval='22',
                                              temperatureFourthWDInterval='20'),
                                    follow_redirects=True)  # Set time intervals(not chronologically) and temperatures
            self.assertIn(b'Time intervals must be set chronologically!',
                          resp.data)  # Verify that the error message is displayed

    def test_setIntervalsWorkingDayTooHighTemperatureValue(self):
        """Verify that if temperature values are too high, an error message will be displayed and
        time intervals and temperatures will not be stored in database"""
        with self.client:
            self.client.post('/',
                             data=dict(username='userNotAdmin', password='userNotAdmin'),
                             follow_redirects=True
                             )  # Log in with a valid account
            self.client.post('/switchIntervalsOn',
                             data=dict(switchIntervalsOn='1'),
                             follow_redirects=True)  # Turn on the automatic mode
            resp = self.client.post('/setIntervalsForWorkingDays',
                                    data=dict(firstWorkingDayInterval='06:00',
                                              secondWorkingDayInterval='08:00',
                                              thirdWorkingDayInterval='16:00',
                                              fourthWorkingDayInterval='22:00',
                                              temperatureFirstWDInterval='34',
                                              temperatureSecondWDInterval='21',
                                              temperatureThirdWDInterval='22',
                                              temperatureFourthWDInterval='20'),
                                    follow_redirects=True)  # Set time intervals and temperatures(at least one value is bigger than 32 degrees)
            self.assertIn(b'The values of temperatures should be between 15 and 32 degrees!',
                          resp.data)  # Verify that the error message is displayed

    def test_setIntervalsWorkingDayTooLowTemperatureValue(self):
        """Verify that if temperature values are too low, an error message will be displayed and
        time intervals and temperatures will not be stored in database"""
        with self.client:
            self.client.post('/',
                             data=dict(username='userNotAdmin', password='userNotAdmin'),
                             follow_redirects=True
                             )  # Log in with a valid account
            self.client.post('/switchIntervalsOn',
                             data=dict(switchIntervalsOn='1'),
                             follow_redirects=True)  # Turn on the automatic mode
            resp = self.client.post('/setIntervalsForWorkingDays',
                                    data=dict(firstWorkingDayInterval='06:00',
                                              secondWorkingDayInterval='08:00',
                                              thirdWorkingDayInterval='16:00',
                                              fourthWorkingDayInterval='22:00',
                                              temperatureFirstWDInterval='22',
                                              temperatureSecondWDInterval='21',
                                              temperatureThirdWDInterval='14',
                                              temperatureFourthWDInterval='20'),
                                    follow_redirects=True)  # Set time intervals and temperatures(at least one value is less than 15 degrees)
            self.assertIn(b'The values of temperatures should be between 15 and 32 degrees!',
                          resp.data)  # Verify that the error message is displayed

    def test_setIntervalsWeekend(self):
        """Verify that the application allows user to set intervals for weekend"""
        with self.client:
            self.client.post('/',
                             data=dict(username='userNotAdmin', password='userNotAdmin'),
                             follow_redirects=True
                             )  # Log in with a valid account
            self.client.post('/switchIntervalsOn',
                             data=dict(switchIntervalsOn='1'),
                             follow_redirects=True)  # Turn on the automatic mode
            resp = self.client.post('/setIntervalsForWeekend',
                                    data=dict(firstWeekendInterval='08:00',
                                              secondWeekendInterval='23:00',
                                              temperatureFirstWInterval='22',
                                              temperatureSecondWInterval='20'
                                              ),
                                    follow_redirects=True)  # Set time intervals and temperatures for weekend
            self.assertIn(b'Intervals were set successfully!',
                          resp.data)  # Verify that the success message is displayed

    def test_setIntervalsWeekendNotChronologically(self):
        """Verify that time intervals are not stored in database if they are not set chronologically"""
        with self.client:
            self.client.post('/',
                             data=dict(username='userNotAdmin', password='userNotAdmin'),
                             follow_redirects=True
                             )  # Log in with a valid account
            self.client.post('/switchIntervalsOn',
                             data=dict(switchIntervalsOn='1'),
                             follow_redirects=True)  # Turn on the automatic mode
            resp = self.client.post('/setIntervalsForWeekend',
                                    data=dict(firstWeekendInterval='23:00',
                                              secondWeekendInterval='08:00',
                                              temperatureFirstWInterval='22',
                                              temperatureSecondWInterval='20'
                                              ),
                                    follow_redirects=True)  # Set time intervals(not chronologically) and temperatures
            self.assertIn(b'Time intervals must be set chronologically!',
                          resp.data)  # Verify that the error message is displayed

    def test_setIntervalsWeekendTooHighTemperature(self):
        """Verify that if temperature values are too high, an error message will be displayed and
        time intervals and temperatures will not be stored in database"""
        with self.client:
            self.client.post('/',
                             data=dict(username='userNotAdmin', password='userNotAdmin'),
                             follow_redirects=True
                             )  # Log in with a valid account
            self.client.post('/switchIntervalsOn',
                             data=dict(switchIntervalsOn='1'),
                             follow_redirects=True)  # Turn on the automatic mode
            resp = self.client.post('/setIntervalsForWeekend',
                                    data=dict(firstWeekendInterval='08:00',
                                              secondWeekendInterval='23:00',
                                              temperatureFirstWInterval='33',
                                              temperatureSecondWInterval='20'
                                              ),
                                    follow_redirects=True)  # Set time intervals and temperatures(at least one value is bigger than 32 degrees)
            self.assertIn(b'The values of temperatures should be between 15 and 32 degrees!',
                          resp.data)  # Verify that the error message is displayed

    def test_setIntervalsWeekendTooLowTemperature(self):
        """Verify that if temperature values are too low, an error message will be displayed and
        time intervals and temperatures will not be stored in database"""
        with self.client:
            self.client.post('/',
                             data=dict(username='userNotAdmin', password='userNotAdmin'),
                             follow_redirects=True
                             )  # Log in with a valid account
            self.client.post('/switchIntervalsOn',
                             data=dict(switchIntervalsOn='1'),
                             follow_redirects=True)  # Turn on the automatic mode
            resp = self.client.post('/setIntervalsForWeekend',
                                    data=dict(firstWeekendInterval='08:00',
                                              secondWeekendInterval='23:00',
                                              temperatureFirstWInterval='22',
                                              temperatureSecondWInterval='14'
                                              ),
                                    follow_redirects=True)  # Set time intervals and temperatures(at least one value is less than 15 degrees)
            self.assertIn(b'The values of temperatures should be between 15 and 32 degrees!',
                          resp.data)  # Verify that the error message is displayed

    def test_changePassword(self):
        """Verify change password functionality"""
        with self.client:
            self.client.post('/',
                             data=dict(username='userNotAdmin', password='userNotAdmin'),
                             follow_redirects=True
                             )  # Log in with a valid account
            resp = self.client.post('/changePassword',
                                    data=dict(currentPassword='userNotAdmin',
                                              newPassword='newPassword1',
                                              confirmNewPassword='newPassword1'),
                                    follow_redirects=True
                                    )  # Try to change the current password
            self.assertIn(b'Password changed successfully!', resp.data)  # Verify that the success message is displayed
            self.assertTrue(bcrypt.check_password_hash(current_user.password,
                                                       'newPassword1'))  # Verify that the password was changed

    def test_changePasswordWrongCurrentPassword(self):
        """Try to change the password when a wrong current password is introduced."""
        with self.client:
            self.client.post('/',
                             data=dict(username='userNotAdmin', password='userNotAdmin'),
                             follow_redirects=True
                             )  # Log in with a valid account
            resp = self.client.post('/changePassword',
                                    data=dict(currentPassword='wrongCurrentPassword',
                                              newPassword='newPassword1',
                                              confirmNewPassword='newPassword1'),
                                    follow_redirects=True
                                    )  # Introduce wrong current password in the change password form
            self.assertIn(b'Wrong password! Please try again!', resp.data)  # Verify that the error message is displayed
            self.assertTrue(bcrypt.check_password_hash(current_user.password,
                                                       'userNotAdmin'))  # Verify that the password was not changed

    def test_changePasswordUnmatchingPasswords_notAdmin(self):
        """Try to change password when the new password and the confirmation do not match"""
        with self.client:
            self.client.post('/',
                             data=dict(username='userNotAdmin', password='userNotAdmin'),
                             follow_redirects=True
                             )  # Log in with a valid account
            resp = self.client.post('/changePassword',
                                    data=dict(currentPassword='userNotAdmin',
                                              newPassword='nePassword1',
                                              confirmNewPassword='newPassword1'),
                                    follow_redirects=True
                                    )  # New password and confirmation do not match
            self.assertIn(b'The passwords do not match!', resp.data)  # Verify that the error message is displayed
            self.assertTrue(bcrypt.check_password_hash(current_user.password,
                                                       'userNotAdmin'))  # Verify that the password was not changed

    def test_changePasswordTooShort(self):
        """Try to change password when the new password is too short"""
        with self.client:
            self.client.post(
                '/',
                data=dict(username="userNotAdmin", password="userNotAdmin"),
                follow_redirects=True
            )  # Log in with a valid account
            resp = self.client.post('/changePassword',
                                    data=dict(currentPassword='userNotAdmin',
                                              newPassword='Shor1',
                                              confirmNewPassword='Shor1',
                                              ),
                                    follow_redirects=True
                                    )  # Introduce a password that is too short
            self.assertIn(b'Password must have at least 6 characters!',
                          resp.data)  # Verify that the error message is displayed
            self.assertTrue(bcrypt.check_password_hash(current_user.password,
                                                       'userNotAdmin'))  # Verify that the password was not changed

    def test_changePasswordMissingUpperCaseLetter(self):
        """Try to change password when the new password does not contain upper case letter"""
        with self.client:
            self.client.post(
                '/',
                data=dict(username="userNotAdmin", password="userNotAdmin"),
                follow_redirects=True
            )  # Log in with a valid account
            resp = self.client.post('/changePassword',
                                    data=dict(currentPassword='userNotAdmin',
                                              newPassword='newuser1',
                                              confirmNewPassword='newuser1',
                                              ),
                                    follow_redirects=True
                                    )  # Introduce new password without containing upper case letter
            self.assertIn(b'The password must contain at least one upper case letter!',
                          resp.data)  # Verify that the error message is displayed
            self.assertTrue(bcrypt.check_password_hash(current_user.password,
                                                       'userNotAdmin'))  # Verify that the password was not changed

    def test_changePasswordMissingDigit(self):
        """Try to change password when the new password does not contain at least one digit"""
        with self.client:
            self.client.post(
                '/',
                data=dict(username="userNotAdmin", password="userNotAdmin"),
                follow_redirects=True
            )  # Log in with a valid account
            resp = self.client.post('/changePassword',
                                    data=dict(currentPassword='userNotAdmin',
                                              newPassword='newUser',
                                              confirmNewPassword='newUser',
                                              ),
                                    follow_redirects=True
                                    )  # Introduce new password without containing at least one digit
            self.assertIn(b'The password must contain at least one digit!',
                          resp.data)  # Verify that the error message is displayed
            self.assertTrue(bcrypt.check_password_hash(current_user.password,
                                                       'userNotAdmin'))  # Verify that the password was not changed

    def test_setTemperatureRoom1(self):
        """Verify set temperature functionality for the first room"""
        with self.client:
            self.client.post('/',
                             data=dict(username='userNotAdmin', password='userNotAdmin'),
                             follow_redirects=True
                             )  # Log in with a valid account
            resp = self.client.post('/home',
                                    data=dict(outputValue1='21'),
                                    follow_redirects=True
                                    )  # Set temperature
            self.assert_status(resp, 200,
                               'Failed to set temperature!')  # Verify if the temperature was set. If 200 html error code is returned, then the value was not saved in database

    def test_setTemperatureRoom2(self):
        """Verify set temperature functionality for the second room"""
        with self.client:
            self.client.post('/',
                             data=dict(username='userNotAdmin', password='userNotAdmin'),
                             follow_redirects=True
                             )  # Log in with a valid account
            resp = self.client.post('/home',
                                    data=dict(outputValue2='22'),
                                    follow_redirects=True
                                    )  # Set temperature
            self.assert_status(resp, 200,
                               'Failed to set temperature!')  # Verify if temperature was set. If 200 http status code is not returned, an error message will be displayed


class UserNotAdminTestCase(BaseTestCase):
    """Verify that an user that is not admin is not allowed to create accounts"""

    def test_notAuthorizedForRegister(self):
        with self.client:
            self.client.post('/',
                             data=dict(username='userNotAdmin', password='userNotAdmin'),
                             follow_redirects=True
                             )  # Log in with a valid account, but without admin rights
            resp = self.client.get('/register', follow_redirects=True)  # Try to access register page
            self.assert_status(resp, 401,
                               'Security error! User without admin rights can access registration page.')  # If 401 http status code is not returned, an error message will be displayed

    def test_notAuthorizedForViewAccounts(self):
        """Verify that an user that is not admin is not allowed to view the list of accounts"""
        with self.client:
            self.client.post('/',
                             data=dict(username='userNotAdmin', password='userNotAdmin'),
                             follow_redirects=True
                             )  # Log in with a valid account, but without admin rights
            resp = self.client.get('/viewAccounts', follow_redirects=True)  # Try to access view accounts page
            self.assert_status(resp, 401,
                               'Security error! User without admin rights can access view accounts page.')  # If 401 http status code is not returned, an error message will be displayed

    def test_notAuthorizedForDeleteAccount(self):
        """Verify that an user that is not admin is not allowed to delete accounts"""
        with self.client:
            self.client.post('/',
                             data=dict(username='userNotAdmin', password='userNotAdmin'),
                             follow_redirects=True
                             )  # Log in with a valid account, but without admin rights
            resp = self.client.get('/deleteAccount/1', follow_redirects=True)  # Try to delete an account
            self.assert_status(resp, 401,
                               'Security error! User without admin rights can delete accounts.')  # If 401 http status code is not returned, an error message will be displayed

    def test_notAuthorizedForGiveAdminRights(self):
        """Verify that an user that is not admin is not allowed to give admin rights to other accounts"""
        with self.client:
            self.client.post('/',
                             data=dict(username='userNotAdmin', password='userNotAdmin'),
                             follow_redirects=True
                             )  # Log in with a valid account, but without admin rights
            resp = self.client.get('/giveAdminRights/1',
                                   follow_redirects=True)  # Try to give admin rights to an account
            self.assert_status(resp, 401,
                               'Security error! User which is not admin can give admin rights to other users.')  # If 401 http status code is not returned, an error message will be displayed

    def test_notAuthorizedForRemoveAdminRights(self):
        """Verify that an user that is not admin is not allowed to remove admin rights from other accounts"""
        with self.client:
            self.client.post('/',
                             data=dict(username='userNotAdmin', password='userNotAdmin'),
                             follow_redirects=True
                             )  # Log in with a valid account, but without admin rights
            resp = self.client.get('/removeAdminRights/1',
                                   follow_redirects=True)  # Try to remove admin rights from an account
            self.assert_status(resp, 401,
                               'Security error! User which is not admin can remove admin rights from other users.')  # If 401 http status code is not returned, an error message will be displayed


class UserAdminTestCase(BaseTestCase):
    def test_registration(self):
        """Verify registration functionality using an admin account"""
        with self.client:
            self.client.post(
                '/',
                data=dict(username="userAdmin", password="userAdmin"),
                follow_redirects=True
            )  # Log in with an admin account
            resp = self.client.post('/register',
                                    data=dict(username='newUser',
                                              password='newUser1',
                                              confirmPassword='newUser1',
                                              admin_role=False),
                                    follow_redirects=True
                                    )  # Try to create new account
            self.assertIn(b'You successfully created a new account!',
                          resp.data)  # Verify that a success message is displayed
            self.assert_status(resp, 200,
                               'Error occured during creating new account!')  # Verify if account was created. If 200 http status code was not returned, an error message will be displayed

    def test_registrationUnmatchingPasswords(self):
        """Try to register when password and confirmation do not match"""
        with self.client:
            self.client.post(
                '/',
                data=dict(username="userAdmin", password="userAdmin"),
                follow_redirects=True
            )  # Log in with an admin account
            resp = self.client.post('/register',
                                    data=dict(username='newUser',
                                              password='newUser1',
                                              confirmPassword='newUser2',
                                              admin_role=False),
                                    follow_redirects=True
                                    )  # Introduce password and confirmPassword that do not match
            self.assertIn(b'The passwords do not match!', resp.data)  # Verify that an error message is displayed
            self.assert_status(resp, 200,
                               'Error occured during creating new account!')  # If 200 http status code is not returned, an error message is displayed

    def test_registrationPasswordTooShort(self):
        """Try to register when password is too short"""
        with self.client:
            self.client.post(
                '/',
                data=dict(username="userAdmin", password="userAdmin"),
                follow_redirects=True
            )  # Log in with an admin account
            resp = self.client.post('/register',
                                    data=dict(username='newUser',
                                              password='Shor1',
                                              confirmPassword='Shor1',
                                              admin_role=False),
                                    follow_redirects=True
                                    )  # Introduce a password that is too short
            self.assertIn(b'Password must have at least 6 characters!',
                          resp.data)  # Verify that an error message is displayed
            self.assert_status(resp, 200,
                               'Error occured during creating new account!')  # If 200 http status code is not returned, an error message is displayed

    def test_registrationMissingUpperCaseLetter(self):
        """Try to register when password is missing upper case letter"""
        with self.client:
            self.client.post(
                '/',
                data=dict(username="userAdmin", password="userAdmin"),
                follow_redirects=True
            )  # Log in with an admin account
            resp = self.client.post('/register',
                                    data=dict(username='newUser',
                                              password='newuser1',
                                              confirmPassword='newuser1',
                                              admin_role=False),
                                    follow_redirects=True
                                    )  # Introduce a password that is missing upper case letter
            self.assertIn(b'The password must contain at least one upper case letter!',
                          resp.data)  # Verify that error message is displayed
            self.assert_status(resp, 200,
                               'Error occured during creating new account!')  # If 200 http status code is not returned, an error message is displayed

    def test_registrationMissingDigit(self):
        """Try to register when password is missing digit"""
        with self.client:
            self.client.post(
                '/',
                data=dict(username="userAdmin", password="userAdmin"),
                follow_redirects=True
            )  # Log in with an admin account
            resp = self.client.post('/register',
                                    data=dict(username='newUser',
                                              password='newUser',
                                              confirmPassword='newUser',
                                              admin_role=False),
                                    follow_redirects=True
                                    )  # Introduce a password that has no digits
            self.assertIn(b'The password must contain at least one digit!',
                          resp.data)  # Verify that error message is displayed
            self.assert_status(resp, 200,
                               'Error occured during creating new account!')  # If 200 http status code is not returned, an error message is displayed

    def test_deleteAccount(self):
        """Verify delete account functionality using an admin account"""
        with self.client:
            self.client.post('/',
                             data=dict(username='userAdmin', password='userAdmin'),
                             follow_redirects=True
                             )  # Log in with an admin account
            resp = self.client.get('/deleteAccount/2', follow_redirects=True)  # Try to delete account
            self.assertIn(b'The account was successfully deleted!',
                          resp.data)  # Verify if the success message is displayed
            self.assert_status(resp, 200,
                               'Error occured during deleting account!')  # If 200 http status code is not returned, an error message is displayed

    def test_deleteAccountDatabaseError(self):
        """Try to delete account that is not in database"""
        with self.client:
            self.client.post('/',
                             data=dict(username='userAdmin', password='userAdmin'),
                             follow_redirects=True
                             )  # Log in with an admin account
            resp = self.client.get('/deleteAccount/10', follow_redirects=True)  # Try to delete account
            self.assertIn(b'There was a problem deleting the account!',
                          resp.data)  # Verify that error message is displayed
            self.assert_status(resp, 200,
                               'Error occured during deleting account!')  # If 200 http status code is not returned, an error message is displayed

    def test_giveAdminRights(self):
        """Verify if an administrator can give admin rights to other user """
        with self.client:
            self.client.post('/',
                             data=dict(username='userAdmin', password='userAdmin'),
                             follow_redirects=True
                             )  # Log in with an admin account
            resp = self.client.get('/giveAdminRights/2',
                                   follow_redirects=True)  # Try to give admin rights to an account
            self.assertIn(b'Succesfully updated the admin rights!',
                          resp.data)  # Verify that success message is displayed
            self.assert_status(resp, 200,
                               'Error occured during giving admin rights to an user account!')  # If 200 http status code is not returned, an error message is displayed

    def test_giveAdminRightsDatabaseError(self):
        """Try to give admin rights to an account that is not in database"""
        with self.client:
            self.client.post('/',
                             data=dict(username='userAdmin', password='userAdmin'),
                             follow_redirects=True
                             )  # Log in with an admin account
            resp = self.client.get('/giveAdminRights/10',
                                   follow_redirects=True)  # Try to give admin rights to non-existent account
            self.assertIn(b'There was a problem updating the admin rights!',
                          resp.data)  # Verify that error message is displayed
            self.assert_status(resp, 200,
                               'Error occured during giving admin rights to an user account!')  # If 200 http status code is not returned, an error message is displayed

    def test_removeAdminRights(self):
        """Verify if an administrator can remove admin rights from other user """
        with self.client:
            self.client.post('/',
                             data=dict(username='userAdmin', password='userAdmin'),
                             follow_redirects=True
                             )  # Log in with an admin account
            resp = self.client.get('/removeAdminRights/3',
                                   follow_redirects=True)  # Try to remove admin rights from an account
            self.assertIn(b'Succesfully updated the admin rights!',
                          resp.data)  # Verify that success message is displayed
            self.assert_status(resp, 200,
                               'Error occured during removing admin rights to an user account!')  # If 200 http status code is not returned, an error message is displayed

    def test_removeAdminRightsDatabaseError(self):
        """Try to remove admin rights from an account that is not in database"""
        with self.client:
            self.client.post('/',
                             data=dict(username='userAdmin', password='userAdmin'),
                             follow_redirects=True
                             )  # Log in with an admin account
            resp = self.client.get('/removeAdminRights/10',
                                   follow_redirects=True)  # Try to remove admin rights from non-existent account
            self.assertIn(b'There was a problem updating the admin rights!',
                          resp.data)  # Verify that error message is displayed
            self.assert_status(resp, 200,
                               'Error occured during removing admin rights to an user account!')  # If 200 http status code is not returned, an error message is displayed


if __name__ == '__main__':
    unittest.main()
