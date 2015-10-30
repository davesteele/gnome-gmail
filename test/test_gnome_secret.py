
import pytest

from gi.repository import Secret

@pytest.fixture
def schema():
    SCHEMA = Secret.Schema.new(
        'com.github.davesteele.oauth2',
        Secret.SchemaFlags.NONE,
        {
            "user":  Secret.SchemaAttributeType.STRING,
            "scope": Secret.SchemaAttributeType.STRING,
        }
    )

    return SCHEMA


@pytest.fixture
def secret_write(schema):
    Secret.password_store_sync(
        schema, {'user': 'user', 'scope': 'scope'},
        Secret.COLLECTION_DEFAULT,
        "foo",
        "value",
    )

    return schema


def test_secret_schema(schema):
    assert schema


def test_secret_store(secret_write):
    pass


def test_secret_read(secret_write):
    schema = secret_write

    password = Secret.password_lookup_sync(schema,
                    {'user': 'user', 'scope': 'scope'}, None
               )

    assert password == 'value'
