from prefect import flow

from prefect_jinja.tasks import (
    goodbye_prefect_jinja,
    hello_prefect_jinja,
)


def test_hello_prefect_jinja():
    @flow
    def test_flow():
        return hello_prefect_jinja()

    result = test_flow()
    assert result == "Hello, prefect-jinja!"


def goodbye_hello_prefect_jinja():
    @flow
    def test_flow():
        return goodbye_prefect_jinja()

    result = test_flow()
    assert result == "Goodbye, prefect-jinja!"
