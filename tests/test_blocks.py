from typing import Dict

from jinja2 import Environment, FileSystemLoader

from prefect_jinja.blocks import JinjaEnvironmentBlock


class TestJinjaEnvironmentBlock:
    def test_initialize_attr_with_defaults(self):
        jinja_env_block = JinjaEnvironmentBlock()
        assert jinja_env_block.search_path is None
        assert isinstance(jinja_env_block.namespace, Dict)

    def test_initialize_attr_from_kwargs(self):
        jinja_env_block = JinjaEnvironmentBlock(search_path="test", namespace={"test": "test"})
        assert jinja_env_block.search_path == "test"
        assert jinja_env_block.namespace["test"] == "test"

    def test_get_env(self):
        jinja_env_block = JinjaEnvironmentBlock(search_path="templates", namespace={"test": "test"})

        jinja_env = jinja_env_block.get_env()
        assert isinstance(jinja_env, Environment)
        assert jinja_env.is_async is True
        assert jinja_env.globals["test"] == "test"

        assert isinstance(jinja_env.loader, FileSystemLoader)
        assert "templates" in jinja_env.loader.searchpath


