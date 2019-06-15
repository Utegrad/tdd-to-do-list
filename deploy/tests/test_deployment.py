import pytest
from deploy.deployment import Deployment, EXCLUDED_FILE_PATTERNS, EXCLUDED_DIRECTORY_PATTERNS

file_names = [
    ('.env', True),
    ('gecko.log', True),
    ('my.db', True),
    ('manage.py', False),
    ('blah', False),
]

directory_names = [
    ('__pycache__', True),
    ('.blah', True),
    ('something', False),
    ('else.dir', False),
    ('C:\\sources\\django_tdd_tutorial\\src\\.ipynb_checkpoints', True)
]


@pytest.mark.parametrize('name, excluded', file_names)
def test_excluded_files(name, excluded):
    assert Deployment.excluded(name, EXCLUDED_FILE_PATTERNS) == excluded


@pytest.mark.parametrize('name, excluded', directory_names)
def test_excluded_directories(name, excluded):
    assert Deployment.excluded(name, EXCLUDED_DIRECTORY_PATTERNS) == excluded
