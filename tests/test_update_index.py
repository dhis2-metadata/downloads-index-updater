import pytest
from update_index import get_or_create_object


@pytest.fixture
def parent_object():
    return [
        {'key': 'value1', 'name': 'object1'},
        {'key': 'value2', 'name': 'object2'}
    ]


def test_get_or_create_object_existing(parent_object):
    existing_object = get_or_create_object(parent_object, 'key', 'value1', {})
    assert existing_object == {'key': 'value1', 'name': 'object1'}


def test_get_or_create_object_new(parent_object):
    new_object = get_or_create_object(parent_object, 'key', 'value3', {'name': 'object3'})
    assert new_object == {'key': 'value3', 'name': 'object3'}
    assert parent_object == [
        {'key': 'value1', 'name': 'object1'},
        {'key': 'value2', 'name': 'object2'},
        {'key': 'value3', 'name': 'object3'}
    ]
