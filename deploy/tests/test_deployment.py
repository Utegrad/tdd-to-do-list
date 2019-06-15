import pytest
from deploy.deployment import Deployment, EXCLUDED_FILE_PATTERNS, EXCLUDED_DIRECTORY_PATTERNS

file_names = [
    ('.env', True),
    ('gecko.log', True),
    ('my.db', True),
    ('manage.py', False),
    ('blah', False),
    (r'/blah/blah', False),
    (r'/foo/bar.baz', False),
    (r'c:\blah\.hidden', True),
    (r'c:\\blah\\.hidden', True),
    (r'/blah/.hidden', True),
    (r'c:\\blah\\blah.ipynb', True),
    (r'/blah/blah.ipynb', True),
]

directory_names = [
    ('__pycache__', True),
    ('.blah', True),
    ('something', False),
    ('else.dir', False),
    ('C:\\sources\\django_tdd_tutorial\\src\\.ipynb_checkpoints', True),
    (r'C:\blah\.hidden', True),
    (r'/blah/.hidden', True),
    ('/foo/bar', False),
    ('/foo/bar.baz', False),
    ('C:\\sources\\django_tdd_tutorial\\src\\django_tdd_tutorial', False),
    ('C:\\sources\\django_tdd_tutorial\\src\\lists', False, ),
    ('C:\\test\\functional_tests', True),
    ('/foo/functional_tests', True),
]


@pytest.mark.parametrize('name, excluded', file_names)
def test_excluded_files(name, excluded):
    assert Deployment.excluded(name, EXCLUDED_FILE_PATTERNS) == excluded


@pytest.mark.parametrize('name, excluded', directory_names)
def test_excluded_directories(name, excluded):
    assert Deployment.excluded(name, EXCLUDED_DIRECTORY_PATTERNS) == excluded
