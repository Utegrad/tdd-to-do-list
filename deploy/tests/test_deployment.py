from unittest import mock

import pytest

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

expected_env_content = [
    (
        "DEBUG=false\r"
        + "SECRET_KEY=some_super_secret_key\r"
        + "DATABASE_URL=database_string\r"
        + "INTERNAL_IPS=127.0.0.1\r"
        + "ALLOWED_HOSTS=localhost,127.0.0.1,foo.bar.com\r"
    ),
]


@pytest.mark.parametrize("name, excluded", file_names)
def test_excluded_files(name, excluded):
    assert Deployment.excluded(name, EXCLUDED_FILE_PATTERNS) == excluded


@pytest.mark.parametrize("name, excluded", directory_names)
def test_excluded_directories(name, excluded):
    assert Deployment.excluded(name, EXCLUDED_DIRECTORY_PATTERNS) == excluded


@mock.patch("deploy.deployment.get_secrets")
def test_env_file_values_for_DotEnvKeys(mock_get_secrets):
    get_secrets_string = """{"SECRET_KEY":"some_super_secret_key",
        "DATABASE_URL":"database_string",
        "APP_PATH":"/foo/bar/app/path",
        "VENV_PATH":"/foo/bar/Envs/tdd",
        "STATIC_PATH":"/foo/bar/static/tdd",
        "MEDIA_PATH":"/foo/bar/media/TDD",
        "DEBUG":"false",
        "INTERNAL_IPS":"127.0.0.1",
        "ALLOWED_HOSTS":"localhost,127.0.0.1,foo.bar.com"}"""
    expected_env_result = {
        "DEBUG": "false",
        "SECRET_KEY": "some_super_secret_key",
        "DATABASE_URL": "database_string",
        "INTERNAL_IPS": "127.0.0.1",
        "ALLOWED_HOSTS": "localhost,127.0.0.1,foo.bar.com",
    }
    mock_get_secrets.return_value = (get_secrets_string, None)
    deployment = Deployment()
    actual_env_result = deployment.env_file_filter_values()
    assert expected_env_result == actual_env_result


@mock.patch("deploy.deployment.get_secrets")
def test_env_file_content(mock_get_secrets):
    get_secrets_string = """{"SECRET_KEY":"some_super_secret_key",
        "DATABASE_URL":"database_string",
        "APP_PATH":"/foo/bar/app/path",
        "VENV_PATH":"/foo/bar/Envs/tdd",
        "STATIC_PATH":"/foo/bar/static/tdd",
        "MEDIA_PATH":"/foo/bar/media/TDD",
        "DEBUG":"false",
        "INTERNAL_IPS":"127.0.0.1",
        "ALLOWED_HOSTS":"localhost,127.0.0.1,foo.bar.com"}"""
    expected_env_content = (
        "DEBUG=false\r"
        + "SECRET_KEY=some_super_secret_key\r"
        + "DATABASE_URL=database_string\r"
        + "INTERNAL_IPS=127.0.0.1\r"
        + "ALLOWED_HOSTS=localhost,127.0.0.1,foo.bar.com\r"
    )
    mock_get_secrets.return_value = (get_secrets_string, None)
    deployment = Deployment()
    actual_env_content = deployment.env_file_content()
    assert expected_env_content == actual_env_content


@mock.patch("deploy.deployment.get_secrets")
def test_write_env_file_content(mock_get_secrets):
    get_secrets_string = """{"SECRET_KEY":"some_super_secret_key",
        "DATABASE_URL":"database_string",
        "APP_PATH":"/foo/bar/app/path",
        "VENV_PATH":"/foo/bar/Envs/tdd",
        "STATIC_PATH":"/foo/bar/static/tdd",
        "MEDIA_PATH":"/foo/bar/media/TDD",
        "DEBUG":"false",
        "INTERNAL_IPS":"127.0.0.1",
        "ALLOWED_HOSTS":"localhost,127.0.0.1,foo.bar.com"}"""
    mock_get_secrets.return_value = (get_secrets_string, None)
    deployment = Deployment()
    m = mock.mock_open()
    with mock.patch("deploy.deployment.open", m, create=True):
        deployment.write_env_file("foo")
    m.assert_called_once_with("foo", "w")
