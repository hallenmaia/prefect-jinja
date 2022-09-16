import pytest
from prefect import flow, task
from prefect.context import get_run_context

from prefect_jinja.blocks import JinjaEnvironmentBlock
from prefect_jinja.tasks import _get_template_context, jinja_render_from_template, jinja_render_from_string


@pytest.fixture(scope="session")
def single_template_file(tmp_path_factory) -> str:
    fn = tmp_path_factory.mktemp("template")
    with open(fn / "single_template.txt", "a") as f:
        f.writelines(
            [
                "Hello, {{username}}!",
                "This is a single template with variable: {{config}}."
            ]
        )

    return str(fn)


@pytest.fixture(scope="session")
def inherited_template_file(tmp_path_factory) -> str:
    fn = tmp_path_factory.mktemp("template")
    with open(fn / "base_template.txt", "a") as f:
        f.writelines(
            [
                "Hello, {{username}}!",
                "{% block variables %}{% endblock %}"
            ]
        )
    with open(fn / "child_template.txt", "a") as f:
        f.writelines(
            [
                "{% extends 'base_template.txt' %}",
                "{% block variables %}This is a inherited template with variable: {{config}}.{% endblock %}"
            ]
        )

    return str(fn)


def test_get_template_context():
    @task(tags=["test"])
    def get_context():
        context = get_run_context()
        return _get_template_context(context)

    @flow
    def test_get_template_context_flow():
        return get_context()

    result = test_get_template_context_flow()
    assert "context" in result
    assert "tags" in result["context"]
    assert ["test"] == result["context"]["tags"]


def test_jinja_render_from_template_with_single_template_file(single_template_file):
    @flow
    def jinja_render_from_template_with_single_template_file_flow():
        jinja_env_block = JinjaEnvironmentBlock(search_path=single_template_file, namespace={"config": "test"})
        return jinja_render_from_template("single_template.txt", jinja_env_block, username="prefect-jinja")

    result = jinja_render_from_template_with_single_template_file_flow()
    assert result == "Hello, prefect-jinja!This is a single template with variable: test."


def test_jinja_render_from_template_with_inherited_template_file(inherited_template_file):
    @flow
    def jinja_render_from_template_with_inherited_template_file_flow():
        jinja_env_block = JinjaEnvironmentBlock(search_path=inherited_template_file, namespace={"config": "test"})
        return jinja_render_from_template("child_template.txt", jinja_env_block, username="prefect-jinja")

    result = jinja_render_from_template_with_inherited_template_file_flow()
    assert result == "Hello, prefect-jinja!This is a inherited template with variable: test."


def test_jinja_render_template_from_string():
    @flow
    def jinja_render_template_from_string_flow():
        return jinja_render_from_string("Hello, {{username}}!", username="prefect-jinja")

    result = jinja_render_template_from_string_flow()
    assert result == "Hello, prefect-jinja!"
