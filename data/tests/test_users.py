import pytest

import data.users as usrs


# Yield a temporary user for testing
@pytest.fixture(scope='function')
def temp_user():
    user = usrs.get_test_user()
    ret = usrs.add_user(user)
    yield user
    if usrs.already_exist(user['email']):
        usrs.del_user(user['email'])


# Assertion:
# User name is a string
# Length of user name is larger than 2
def test_get_test_name():
    name = usrs._get_test_name()
    assert isinstance(name, str)
    assert len(name) > 2


# Assertion:
# User email is a string
# Length of user email is larger than 0
# In user email, there is @ and characters before @
# Make sure the email address is valid
def test_get_test_email():
    email = usrs._get_test_email()
    assert isinstance(email, str)
    assert len(email) > 0
    assert '@' in email
    email_components = email.split('@')
    assert len(email_components[0]) >= 1
    assert '.' in email_components[1]


# Assertion:
# User password is a string
# Length of password is larger than required minimum length
def test_get_test_password():
    password = usrs._get_test_password()
    assert isinstance(password, str)
    assert len(password) >= usrs.MIN_PW_LEN


# Assertion:
# User is a dictionary
def test_get_test_user():
    assert isinstance(usrs.get_test_user(), dict)


# Assertion:
# Fetched user is a string
# Length of fetched user is larger than 0
# In the user dictionary, each value meet requirement
def test_get_users():
    users = usrs.get_users()
    assert isinstance(users, dict)
    assert len(users) >= 0
    for key in users:
        assert isinstance(key, str)
        assert '@' in key
        email_components = key.split('@')
        assert len(email_components[0]) >= 1
        assert '.' in email_components[1]
        user = users[key]
        assert usrs.NAME in user
        assert isinstance(user[usrs.NAME], str)
        assert len(user[usrs.NAME]) >= usrs.MIN_USER_NAME_LEN
        assert isinstance(user, dict)
        assert usrs.EMAIL in user
        assert isinstance(user[usrs.EMAIL], str)
        assert usrs.PASSWORD in user
        assert isinstance(user[usrs.PASSWORD], str)
        assert len(user[usrs.PASSWORD]) >= usrs.MIN_PW_LEN


# Assertion:
# If the temporary user has already existed in the databse, delete it
def test_already_exist(temp_user):
    email = temp_user['email']
    assert usrs.already_exist(email) is True
    usrs.del_user(email)


# For tested user that is new in the database
# Assertion: False
def test_already_exist_not_there():
    new_name = usrs._get_test_name()
    new_email = usrs._get_test_email()
    new_password = usrs._get_test_password()
    new_user = {
        'name': new_name,
        'email': new_email,
        'password': new_password,
    }
    assert usrs.already_exist(new_email) is False


# Test the new user
# If the new user already exist, delete the new user
def test_add_user():
    new_name = usrs._get_test_name()
    new_email = usrs._get_test_email()
    new_password = usrs._get_test_password()
    new_user = {
        'name': new_name,
        'email': new_email,
        'password': new_password,
    }
    ret = usrs.add_user(new_user)
    assert usrs.already_exist(new_user['email'])
    assert isinstance(ret, bool)
    usrs.del_user(new_user['email'])


# Test adding new user with duplicate email
def test_add_user_dup_email(temp_user):
    with pytest.raises(ValueError):
        usrs.add_user(temp_user)


# Test adding new user with length less than two characters
def test_add_user_lt_2_char():
    new_name = 'w'
    new_email = usrs._get_test_email()
    new_password = usrs._get_test_password()
    new_user = {
        'name': new_name,
        'email': new_email,
        'password': new_password,
    }
    with pytest.raises(ValueError):
        usrs.add_user(new_user)


# Test adding new user with an invalid email
def test_add_user_invalid_email():
    new_name = usrs._get_test_name()
    new_email = 'randomstring'
    new_password = usrs._get_test_password()
    new_user = {
        'name': new_name,
        'email': new_email,
        'password': new_password,
    }
    with pytest.raises(ValueError):
        usrs.add_user(new_user)


# Test adding new user with an invalid password
# Specifically the password length is smaller than required minimum length
def test_add_user_invalid_password():
    new_name = usrs._get_test_name()
    new_email = usrs._get_test_email()
    new_password = "1234567"
    new_user = {
        'name': new_name,
        'email': new_email,
        'password': new_password,
    }
    with pytest.raises(ValueError):
        usrs.add_user(new_user)


# Assertion:
# The user is new in the database
def test_del_user(temp_user):
    email = temp_user['email']
    usrs.del_user(email)
    assert usrs.already_exist(email) is False


# Test deleting user that is not in the database
def test_del_user_not_there():
    email = usrs._get_test_email()
    with pytest.raises(ValueError):
        usrs.del_user(email)


# Test matching user email and password
# Assertion:
# Only user with the righ email and password is True
def test_auth_user(temp_user):
    right_email = temp_user['email']
    right_password = temp_user['password']
    wrong_email = "somewrongemail"
    wrong_password = "songwrongpassword"
    assert usrs.auth_user(right_email, right_password) is True
    assert usrs.auth_user(wrong_email, right_password) is False
    assert usrs.auth_user(right_email, wrong_password) is False
    assert usrs.auth_user(wrong_email, wrong_password) is False
    assert len(right_password) >= 8


# Test matching user email and password with password length 
# smaller than required minimum length
def test_auth_user_invalid_password_length(temp_user):
    right_email = temp_user['email']
    right_password = temp_user['password']
    wrong_password = "1234567"
    assert usrs.auth_user(right_email, right_password) is True
    with pytest.raises(ValueError):
        usrs.auth_user(right_email, wrong_password)
