import pytest

import data.users as usrs


@pytest.fixture(scope='function')
def temp_user():
    user = usrs.get_test_user()
    ret = usrs.add_user(user)
    yield user
    if usrs.already_exist(user['email']):
        usrs.del_user(user['email'])


def test_get_test_name():
    name = usrs._get_test_name()
    assert isinstance(name, str)
    assert len(name) > 2


def test_get_test_email():
    email = usrs._get_test_email()
    assert isinstance(email, str)
    assert len(email) > 0
    assert '@' in email


def test_get_test_password():
    password = usrs._get_test_password()
    assert isinstance(password, str)
    assert len(password) >= usrs.MIN_PW_LEN


def test_get_test_user():
    assert isinstance(usrs.get_test_user(), dict)


def test_get_users():
    users = usrs.get_users()
    assert isinstance(users, dict)
    assert len(users) >= 0
    for key in users:
        assert isinstance(key, str)
        assert '@' in key
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


def test_add_user_dup_email(temp_user):
    with pytest.raises(ValueError):
        usrs.add_user(temp_user)


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


def test_del_user(temp_user):
    email = temp_user['email']
    usrs.del_user(email)
    assert usrs.already_exist(email) is False


def test_del_user_not_there():
    email = usrs._get_test_email()
    with pytest.raises(ValueError):
        usrs.del_user(email)


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


def test_auth_user_invalid_password_length(temp_user):
    right_email = temp_user['email']
    right_password = temp_user['password']
    wrong_password = "1234567"
    assert usrs.auth_user(right_email, right_password) is True
    with pytest.raises(ValueError):
        usrs.auth_user(right_email, wrong_password)