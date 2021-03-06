from unittest import mock

import pytest
from fabric import Connection

from deploy.deployment import (
    Deployment,
    EXCLUDED_FILE_PATTERNS,
    EXCLUDED_DIRECTORY_PATTERNS,
)

file_names = [
    (".env", True),
    ("gecko.log", True),
    ("my.db", True),
    ("manage.py", False),
    ("blah", False),
    (r"/blah/blah", False),
    (r"/foo/bar.baz", False),
    (r"c:\blah\.hidden", True),
    (r"c:\\blah\\.hidden", True),
    (r"/blah/.hidden", True),
    (r"c:\\blah\\blah.ipynb", True),
    (r"/blah/blah.ipynb", True),
]

directory_names = [
    ("__pycache__", True),
    (".blah", True),
    ("something", False),
    ("else.dir", False),
    ("C:\\sources\\django_tdd_tutorial\\src\\.ipynb_checkpoints", True),
    (r"C:\blah\.hidden", True),
    (r"/blah/.hidden", True),
    ("/foo/bar", False),
    ("/foo/bar.baz", False),
    ("C:\\sources\\django_tdd_tutorial\\src\\django_tdd_tutorial", False),
    ("C:\\sources\\django_tdd_tutorial\\src\\lists", False),
    ("C:\\test\\functional_tests", True),
    ("/foo/functional_tests", True),
]

example_secrets_value: str = (
    '{"SECRET_KEY":"some_super_secret_key",'
    + '"DATABASE_URL":"database_string",'
    + '"APP_PATH":"/foo/bar/app/path/",'
    + '"VENV_PATH":"/foo/bar/Envs/tdd/",'
    + '"STATIC_ROOT":"/foo/bar/static/tdd/",'
    + '"MEDIA_ROOT":"/foo/bar/media/tdd/",'
    + '"DEBUG":"false",'
    + '"INTERNAL_IPS":"127.0.0.1",'
    + '"ALLOWED_HOSTS":"localhost,127.0.0.1,foo.bar.com",'
    + '"DJANGO_SETTINGS_DIR":"some/directory"}'
)

example_env_content: str = (
    "DEBUG=false\n"
    + "SECRET_KEY=some_super_secret_key\n"
    + "DATABASE_URL=database_string\n"
    + "INTERNAL_IPS=127.0.0.1\n"
    + "ALLOWED_HOSTS=localhost,127.0.0.1,foo.bar.com\n"
    + "STATIC_ROOT=/foo/bar/static/tdd/\n"
    + "MEDIA_ROOT=/foo/bar/media/tdd/\n"
)

expected_env_content = [(example_secrets_value, example_env_content)]
expected_secrets = [example_secrets_value]


@pytest.mark.parametrize("name, excluded", file_names)
def test_excluded_files(name, excluded):
    assert Deployment.excluded(name, EXCLUDED_FILE_PATTERNS) == excluded


@pytest.mark.parametrize("name, excluded", directory_names)
def test_excluded_directories(name, excluded):
    assert Deployment.excluded(name, EXCLUDED_DIRECTORY_PATTERNS) == excluded


@pytest.mark.parametrize("secrets", expected_secrets)
@mock.patch("deploy.deployment.get_secrets")
def test_env_file_values_for_DotEnvKeys(mock_get_secrets, secrets):
    get_secrets_string = secrets
    expected_env_result = {
        "DEBUG": "false",
        "SECRET_KEY": "some_super_secret_key",
        "DATABASE_URL": "database_string",
        "INTERNAL_IPS": "127.0.0.1",
        "ALLOWED_HOSTS": "localhost,127.0.0.1,foo.bar.com",
        "STATIC_ROOT": "/foo/bar/static/tdd/",
        "MEDIA_ROOT": "/foo/bar/media/tdd/",
    }
    mock_get_secrets.return_value = (get_secrets_string, None)
    deployment = Deployment()
    actual_env_result = deployment.env_file_filter_values()
    assert expected_env_result == actual_env_result


@pytest.mark.parametrize("secrets_value, content", expected_env_content)
@mock.patch("deploy.deployment.get_secrets")
def test_env_file_content(mock_get_secrets, secrets_value, content):
    get_secrets_string = secrets_value
    mock_get_secrets.return_value = (get_secrets_string, None)
    deployment = Deployment()
    actual_env_content = deployment.env_file_content()
    assert content == actual_env_content


@pytest.mark.parametrize("secrets", expected_secrets)
@mock.patch("deploy.deployment.get_secrets")
def test_write_env_file_content(mock_get_secrets, secrets):
    get_secrets_string = secrets
    mock_get_secrets.return_value = (get_secrets_string, None)
    deployment = Deployment()
    m = mock.mock_open()
    with mock.patch("deploy.deployment.open", m, create=True):
        deployment.write_env_file("foo")
    m.assert_called_once_with("foo", "w")

@pytest.mark.skip('Not sure how to mock the put')
@pytest.mark.parametrize("secrets", expected_secrets)
def test_copy_env_file_calls_put(secrets):
    with mock.patch("deploy.deployment.Connection", spec=Connection) as m_connection:
        with mock.patch("deploy.deployment.get_secrets") as m_get_secrets:
            m_get_secrets.return_value = (secrets, None)
            d = Deployment()
            d.copy_env_file("env_file")
            m_connection.put.assert_called_once()
