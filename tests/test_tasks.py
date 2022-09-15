import pytest
from prefect import flow

from prefect_jinja.blocks import JinjaEnvironmentBlock
from prefect_jinja.tasks import jinja_render_from_template, jinja_render_from_string


@pytest.fixture(scope="session")
def template_path(tmp_path_factory) -> str:
    fn = tmp_path_factory.mktemp("template")
    # Single template
    with open(fn / "single_template.txt", "a") as f:
        f.writelines(
            [
                "Hello, {{username}}!",
                "This is a single template with variable: {{config}}."
            ]
        )
    # Template Inheritance
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


def test_jinja_render_from_template(template_path):
    @flow
    def test_flow_jinja_render_from_single_template():
        jinja_env_block = JinjaEnvironmentBlock(search_path=template_path, namespace={"config": "test"})
        return jinja_render_from_template("single_template.txt", jinja_env_block, username="prefect-jinja")

    result = test_flow_jinja_render_from_single_template()
    assert result == "Hello, prefect-jinja!This is a single template with variable: test."

    @flow
    def test_flow_jinja_render_from_inherited_template():
        jinja_env_block = JinjaEnvironmentBlock(search_path=template_path, namespace={"config": "test"})
        return jinja_render_from_template("child_template.txt", jinja_env_block, username="prefect-jinja")

    result = test_flow_jinja_render_from_inherited_template()
    assert result == "Hello, prefect-jinja!This is a inherited template with variable: test."


def test_jinja_render_template_from_string():
    @flow
    def test_flow_jinja_render_template_from_string():
        return jinja_render_from_string("Hello, {{username}}!", username="prefect-jinja")

    result = test_flow_jinja_render_template_from_string()
    assert result == "Hello, prefect-jinja!"
