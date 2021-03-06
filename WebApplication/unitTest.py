import os
import unittest
from flask_testing import TestCase
from app import app, db, Users, bcrypt, current_user


class BaseTestCase(TestCase):
    def create_app(self):
        app.config['DEBUG'] = True
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['SECRET_KEY'] = str(os.environ.get("FLASK_SECRET_KEY"))
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        return app

    def setUp(self):
        db.create_all()
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
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()


class CommonTestCase(BaseTestCase):
    def test_loginIsRequired_home(self):
        resp = self.client.get('/home', follow_redirects=True)
        self.assert_status(resp, 401,
                           'Security error! Home page can be accessed by users that are not logged in.')

    def test_loginIsRequired_register(self):
        resp = self.client.get('/register', follow_redirects=True)
        self.assert_status(resp, 401,
                           'Security error! Register page can be accessed by users that are not logged in.')

    def test_loginIsRequired_viewAccounts(self):
        resp = self.client.get('/viewAccounts', follow_redirects=True)
        self.assert_status(resp, 401,
                           'Security error! View accounts page can be accessed by users that are not logged in.')

    def test_loginIsRequired_delteAccount(self):
        resp = self.client.get('/deleteAccount/1', follow_redirects=True)
        self.assert_status(resp, 401,
                           'Security error! Accounts can be deleted by users which are not logged in.')

    def test_loginIsRequired_giveAdminRights(self):
        resp = self.client.get('/giveAdminRights/1', follow_redirects=True)
        self.assert_status(resp, 401,
                           'Security error! An user which is not logged in can give admin rights to other accounts.')

    def test_loginIsRequired_removeAdminRights(self):
        resp = self.client.get('/removeAdminRights/1', follow_redirects=True)
        self.assert_status(resp, 401,
                           'Security error! An user which is not logged in can remove admin rights from other accounts')

    def test_loginIsRequired_changePassword(self):
        resp = self.client.get('/changePassword', follow_redirects=True)
        self.assert_status(resp, 401,
                           'Security error! Change password page can be accessed by users that are not logged in.')

    def test_loginIsRequired_switchIntervalsOn(self):
        resp = self.client.get('/switchIntervalsOn', follow_redirects=True)
        self.assert_status(resp, 401,
                           'Security error! Intervals can be switched on or off by users which are not logged in.')

    def test_loginIsRequired_setIntervalsForWorkingDays(self):
        resp = self.client.get('/setIntervalsForWorkingDays', follow_redirects=True)
        self.assert_status(resp, 401,
                           'Security error! Intervals for working days can be set by users which are not logged in.')

    def test_loginIsRequired_setIntervalsForWeekend(self):
        resp = self.client.get('/setIntervalsForWeekend', follow_redirects=True)
        self.assert_status(resp, 401,
                           'Security error! Intervals for weekend can be set by users which are not logged in.')

    def test_loginIsRequired_logOut(self):
        resp = self.client.get('/logout', follow_redirects=True)
        self.assert_status(resp, 401,
                           'Security error! An user can logout without being logged in.')

    def test_notExistentAccount(self):
        with self.client:
            resp = self.client.post('/',
                                    data=dict(username='notPresentInDatabase', password='notPresentInDatabase'),
                                    follow_redirects=True
                                    )
            self.assertIn(
                b'This account does not exist in our database! Please contact the administrator for creating one!',
                resp.data)
            self.assertFalse(current_user.is_authenticated)

    def test_passwordEncryption(self):
        with self.client:
            self.client.post(
                '/',
                data=dict(username="userAdmin", password="userAdmin"),
                follow_redirects=True
            )
            self.assertTrue(bcrypt.check_password_hash(current_user.password, 'userAdmin'))
            self.assertFalse(bcrypt.check_password_hash(current_user.password, 'wrongPassword'))

            # -----------#

    def test_login(self):
        with self.client:
            resp = self.client.post('/',
                                    data=dict(username='userNotAdmin', password='userNotAdmin'),
                                    follow_redirects=True
                                    )
            self.assertIn(b'Switch intervals on/off', resp.data)
            self.assertTrue(current_user.username == 'userNotAdmin')
            self.assertTrue(current_user.is_authenticated)

    def test_incorrectLogin(self):
        with self.client:
            resp = self.client.post('/',
                                    data=dict(username='userNotAdmin', password='incorrectPassword'),
                                    follow_redirects=True
                                    )
            self.assertIn(b'Username', resp.data)
            self.assertFalse(current_user.is_authenticated)

    def test_logOut(self):
        with self.client:
            self.client.post('/',
                             data=dict(username='userNotAdmin', password='userNotAdmin'),
                             follow_redirects=True
                             )
            resp = self.client.get('/logout', follow_redirects=True)
            self.assertIn(b'Username', resp.data)
            self.assertFalse(current_user.is_authenticated)

    def test_swithIntervalsOn(self):
        with self.client:
            self.client.post('/',
                             data=dict(username='userNotAdmin', password='userNotAdmin'),
                             follow_redirects=True
                             )
            resp = self.client.post('/switchIntervalsOn',
                                    data=dict(switchIntervalsOn='1'),
                                    follow_redirects=True)
            self.assertTrue(b'Schedule' in resp.data)

    def test_swithIntervalsOff(self):
        with self.client:
            self.client.post('/',
                             data=dict(username='userNotAdmin', password='userNotAdmin'),
                             follow_redirects=True
                             )
            resp = self.client.post('/switchIntervalsOn',
                                    data=dict(switchIntervalsOn='0'),
                                    follow_redirects=True)
            self.assertFalse(b'Schedule' in resp.data)

    def test_setIntervalsWorkingDay(self):
        with self.client:
            self.client.post('/',
                             data=dict(username='userNotAdmin', password='userNotAdmin'),
                             follow_redirects=True
                             )
            self.client.post('/switchIntervalsOn',
                             data=dict(switchIntervalsOn='1'),
                             follow_redirects=True)
            resp = self.client.post('/setIntervalsForWorkingDays',
                                    data=dict(firstWorkingDayInterval='06:00',
                                              secondWorkingDayInterval='08:00',
                                              thirdWorkingDayInterval='16:00',
                                              fourthWorkingDayInterval='22:00',
                                              temperatureFirstWDInterval='22',
                                              temperatureSecondWDInterval='21',
                                              temperatureThirdWDInterval='22',
                                              temperatureFourthWDInterval='20'),
                                    follow_redirects=True)
            self.assertIn(b'Intervals were set successfully!', resp.data)

    def test_setIntervalsWorkingDayNotChronologically(self):
        with self.client:
            self.client.post('/',
                             data=dict(username='userNotAdmin', password='userNotAdmin'),
                             follow_redirects=True
                             )
            self.client.post('/switchIntervalsOn',
                             data=dict(switchIntervalsOn='1'),
                             follow_redirects=True)
            resp = self.client.post('/setIntervalsForWorkingDays',
                                    data=dict(firstWorkingDayInterval='08:00',
                                              secondWorkingDayInterval='06:00',
                                              thirdWorkingDayInterval='22:00',
                                              fourthWorkingDayInterval='16:00',
                                              temperatureFirstWDInterval='22',
                                              temperatureSecondWDInterval='21',
                                              temperatureThirdWDInterval='22',
                                              temperatureFourthWDInterval='20'),
                                    follow_redirects=True)
            self.assertIn(b'Time intervals must be set chronologically!', resp.data)

    def test_setIntervalsWeekend(self):
        with self.client:
            self.client.post('/',
                             data=dict(username='userNotAdmin', password='userNotAdmin'),
                             follow_redirects=True
                             )
            self.client.post('/switchIntervalsOn',
                             data=dict(switchIntervalsOn='1'),
                             follow_redirects=True)
            resp = self.client.post('/setIntervalsForWeekend',
                                    data=dict(firstWeekendInterval='08:00',
                                              secondWeekendInterval='23:00',
                                              temperatureFirstWInterval='22',
                                              temperatureSecondWInterval='20'
                                              ),
                                    follow_redirects=True)
            self.assertIn(b'Intervals were set successfully!', resp.data)

    def test_setIntervalsWeekendNotChronologically(self):
        with self.client:
            self.client.post('/',
                             data=dict(username='userNotAdmin', password='userNotAdmin'),
                             follow_redirects=True
                             )
            self.client.post('/switchIntervalsOn',
                             data=dict(switchIntervalsOn='1'),
                             follow_redirects=True)
            resp = self.client.post('/setIntervalsForWeekend',
                                    data=dict(firstWeekendInterval='23:00',
                                              secondWeekendInterval='08:00',
                                              temperatureFirstWInterval='22',
                                              temperatureSecondWInterval='20'
                                              ),
                                    follow_redirects=True)
            self.assertIn(b'Time intervals must be set chronologically!', resp.data)

    def test_changePassword(self):
        with self.client:
            self.client.post('/',
                             data=dict(username='userNotAdmin', password='userNotAdmin'),
                             follow_redirects=True
                             )
            resp = self.client.post('/changePassword',
                                    data=dict(currentPassword='userNotAdmin',
                                              newPassword='newPassword1',
                                              confirmNewPassword='newPassword1'),
                                    follow_redirects=True
                                    )
            self.assertIn(b'Password changed successfully!', resp.data)
            self.assertTrue(bcrypt.check_password_hash(current_user.password, 'newPassword1'))

    def test_changePasswordWrongCurrentPassword(self):
        with self.client:
            self.client.post('/',
                             data=dict(username='userNotAdmin', password='userNotAdmin'),
                             follow_redirects=True
                             )
            resp = self.client.post('/changePassword',
                                    data=dict(currentPassword='wrongCurrentPassword',
                                              newPassword='newPassword1',
                                              confirmNewPassword='newPassword1'),
                                    follow_redirects=True
                                    )
            self.assertIn(b'Wrong password! Please try again!', resp.data)
            self.assertTrue(bcrypt.check_password_hash(current_user.password, 'userNotAdmin'))

    def test_changePasswordUnmatchingPasswords_notAdmin(self):
        with self.client:
            self.client.post('/',
                             data=dict(username='userNotAdmin', password='userNotAdmin'),
                             follow_redirects=True
                             )
            resp = self.client.post('/changePassword',
                                    data=dict(currentPassword='userNotAdmin',
                                              newPassword='nePassword1',
                                              confirmNewPassword='newPassword1'),
                                    follow_redirects=True
                                    )
            self.assertIn(b'The passwords do not match!', resp.data)
            self.assertTrue(bcrypt.check_password_hash(current_user.password, 'userNotAdmin'))

    def test_changePasswordTooShort(self):
        with self.client:
            self.client.post(
                '/',
                data=dict(username="userNotAdmin", password="userNotAdmin"),
                follow_redirects=True
            )
            resp = self.client.post('/changePassword',
                                    data=dict(currentPassword='userNotAdmin',
                                              newPassword='Shor1',
                                              confirmNewPassword='Shor1',
                                              ),
                                    follow_redirects=True
                                    )
            self.assertIn(b'Password must have at least 6 characters!', resp.data)
            self.assert_status(resp, 200, 'Error occured during creating new account!')

    def test_changePasswordMissingUpperCaseLetter(self):
        with self.client:
            self.client.post(
                '/',
                data=dict(username="userNotAdmin", password="userNotAdmin"),
                follow_redirects=True
            )
            resp = self.client.post('/changePassword',
                                    data=dict(currentPassword='userNotAdmin',
                                              newPassword='newuser1',
                                              confirmNewPassword='newuser1',
                                              ),
                                    follow_redirects=True
                                    )
            self.assertIn(b'The password must contain at least one upper case letter!', resp.data)
            self.assert_status(resp, 200, 'Error occured during creating new account!')

    def test_changePasswordMissingDigit(self):
        with self.client:
            self.client.post(
                '/',
                data=dict(username="userNotAdmin", password="userNotAdmin"),
                follow_redirects=True
            )
            resp = self.client.post('/changePassword',
                                    data=dict(currentPassword='userNotAdmin',
                                              newPassword='newUser',
                                              confirmNewPassword='newUser',
                                              ),
                                    follow_redirects=True
                                    )
            self.assertIn(b'The password must contain at least one digit!', resp.data)
            self.assert_status(resp, 200, 'Error occured during creating new account!')

    def test_setTemperatureRoom1(self):
        with self.client:
            self.client.post('/',
                             data=dict(username='userNotAdmin', password='userNotAdmin'),
                             follow_redirects=True
                             )
            resp = self.client.post('/home',
                                    data=dict(outputValue1='21'),
                                    follow_redirects=True
                                    )
            self.assert_status(resp, 200, 'Failed to set temperature!')

    def test_setTemperatureRoom2(self):
        with self.client:
            self.client.post('/',
                             data=dict(username='userNotAdmin', password='userNotAdmin'),
                             follow_redirects=True
                             )
            resp = self.client.post('/home',
                                    data=dict(outputValue2='22'),
                                    follow_redirects=True
                                    )
            self.assert_status(resp, 200, 'Failed to set temperature!')

            # -----------#


class UserNotAdminTestCase(BaseTestCase):
    def test_notAuthorizedForRegister(self):
        with self.client:
            self.client.post('/',
                             data=dict(username='userNotAdmin', password='userNotAdmin'),
                             follow_redirects=True
                             )
            resp = self.client.get('/register', follow_redirects=True)
            self.assert_status(resp, 401, 'Security error! User without admin rights can access registration page.')

    def test_notAuthorizedForViewAccounts(self):
        with self.client:
            self.client.post('/',
                             data=dict(username='userNotAdmin', password='userNotAdmin'),
                             follow_redirects=True
                             )
            resp = self.client.get('/viewAccounts', follow_redirects=True)
            self.assert_status(resp, 401, 'Security error! User without admin rights can access view accounts page.')

    def test_notAuthorizedForDeleteAccount(self):
        with self.client:
            self.client.post('/',
                             data=dict(username='userNotAdmin', password='userNotAdmin'),
                             follow_redirects=True
                             )
            resp = self.client.get('/deleteAccount/1', follow_redirects=True)
            self.assert_status(resp, 401, 'Security error! User without admin rights can delete accounts.')

    def test_notAuthorizedForGiveAdminRights(self):
        with self.client:
            self.client.post('/',
                             data=dict(username='userNotAdmin', password='userNotAdmin'),
                             follow_redirects=True
                             )
            resp = self.client.get('/giveAdminRights/1', follow_redirects=True)
            self.assert_status(resp, 401,
                               'Security error! User which is not admin can give admin rights to other users.')

    def test_notAuthorizedForRemoveAdminRights(self):
        with self.client:
            self.client.post('/',
                             data=dict(username='userNotAdmin', password='userNotAdmin'),
                             follow_redirects=True
                             )
            resp = self.client.get('/removeAdminRights/1', follow_redirects=True)
            self.assert_status(resp, 401,
                               'Security error! User which is not admin can remove admin rights from other users.')


class UserAdminTestCase(BaseTestCase):
    def test_registration(self):
        with self.client:
            self.client.post(
                '/',
                data=dict(username="userAdmin", password="userAdmin"),
                follow_redirects=True
            )
            resp = self.client.post('/register',
                                    data=dict(username='newUser',
                                              password='newUser1',
                                              confirmPassword='newUser1',
                                              admin_role=False),
                                    follow_redirects=True
                                    )
            self.assertIn(b'You successfully created a new account!', resp.data)
            self.assert_status(resp, 200, 'Error occured during creating new account!')

    def test_registrationUnmatchingPasswords(self):
        with self.client:
            self.client.post(
                '/',
                data=dict(username="userAdmin", password="userAdmin"),
                follow_redirects=True
            )
            resp = self.client.post('/register',
                                    data=dict(username='newUser',
                                              password='newUser1',
                                              confirmPassword='newUser2',
                                              admin_role=False),
                                    follow_redirects=True
                                    )
            self.assertIn(b'The passwords do not match!', resp.data)
            self.assert_status(resp, 200, 'Error occured during creating new account!')

    def test_registrationPasswordTooShort(self):
        with self.client:
            self.client.post(
                '/',
                data=dict(username="userAdmin", password="userAdmin"),
                follow_redirects=True
            )
            resp = self.client.post('/register',
                                    data=dict(username='newUser',
                                              password='Shor1',
                                              confirmPassword='Shor1',
                                              admin_role=False),
                                    follow_redirects=True
                                    )
            self.assertIn(b'Password must have at least 6 characters!', resp.data)
            self.assert_status(resp, 200, 'Error occured during creating new account!')

    def test_registrationMissingUpperCaseLetter(self):
        with self.client:
            self.client.post(
                '/',
                data=dict(username="userAdmin", password="userAdmin"),
                follow_redirects=True
            )
            resp = self.client.post('/register',
                                    data=dict(username='newUser',
                                              password='newuser1',
                                              confirmPassword='newuser1',
                                              admin_role=False),
                                    follow_redirects=True
                                    )
            self.assertIn(b'The password must contain at least one upper case letter!', resp.data)
            self.assert_status(resp, 200, 'Error occured during creating new account!')

    def test_registrationMissingDigit(self):
        with self.client:
            self.client.post(
                '/',
                data=dict(username="userAdmin", password="userAdmin"),
                follow_redirects=True
            )
            resp = self.client.post('/register',
                                    data=dict(username='newUser',
                                              password='newUser',
                                              confirmPassword='newUser',
                                              admin_role=False),
                                    follow_redirects=True
                                    )
            self.assertIn(b'The password must contain at least one digit!', resp.data)
            self.assert_status(resp, 200, 'Error occured during creating new account!')

    def test_deleteAccount(self):
        with self.client:
            self.client.post('/',
                             data=dict(username='userAdmin', password='userAdmin'),
                             follow_redirects=True
                             )
            resp = self.client.get('/deleteAccount/2', follow_redirects=True)
            self.assertIn(b'The account was successfully deleted!', resp.data)
            self.assert_status(resp, 200, 'Error occured during deleting account!')

    def test_deleteAccountDatabaseError(self):
        with self.client:
            self.client.post('/',
                             data=dict(username='userAdmin', password='userAdmin'),
                             follow_redirects=True
                             )
            resp = self.client.get('/deleteAccount/10', follow_redirects=True)
            self.assertIn(b'There was a problem deleting the account!', resp.data)
            self.assert_status(resp, 200, 'Error occured during deleting account!')

    def test_giveAdminRights(self):
        with self.client:
            self.client.post('/',
                             data=dict(username='userAdmin', password='userAdmin'),
                             follow_redirects=True
                             )
            resp = self.client.get('/giveAdminRights/2', follow_redirects=True)
            self.assertIn(b'Succesfully updated the admin rights!', resp.data)
            self.assert_status(resp, 200,
                               'Error occured during giving admin rights to an user account!')

    def test_giveAdminRightsDatabaseError(self):
        with self.client:
            self.client.post('/',
                             data=dict(username='userAdmin', password='userAdmin'),
                             follow_redirects=True
                             )
            resp = self.client.get('/giveAdminRights/10', follow_redirects=True)
            self.assertIn(b'There was a problem updating the admin rights!', resp.data)
            self.assert_status(resp, 200,
                               'Error occured during giving admin rights to an user account!')

    def test_removeAdminRights(self):
        with self.client:
            self.client.post('/',
                             data=dict(username='userAdmin', password='userAdmin'),
                             follow_redirects=True
                             )
            resp = self.client.get('/removeAdminRights/3', follow_redirects=True)
            self.assertIn(b'Succesfully updated the admin rights!', resp.data)
            self.assert_status(resp, 200,
                               'Error occured during removing admin rights to an user account!')

    def test_removeAdminRightsDatabaseError(self):
        with self.client:
            self.client.post('/',
                             data=dict(username='userAdmin', password='userAdmin'),
                             follow_redirects=True
                             )
            resp = self.client.get('/removeAdminRights/10', follow_redirects=True)
            self.assertIn(b'There was a problem updating the admin rights!', resp.data)
            self.assert_status(resp, 200,
                               'Error occured during removing admin rights to an user account!')


if __name__ == '__main__':
    unittest.main()
