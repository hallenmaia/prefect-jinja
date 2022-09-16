"""A module to interact with Jinja Environment."""
from typing import Dict, Optional

from jinja2 import Environment, FileSystemLoader, select_autoescape
from prefect.blocks.core import Block
from pydantic import Field


class JinjaEnvironmentBlock(Block):
    """
    Block to create a template environment.

    Stores the path where the templates files are stored and also the variables that will be available in all templates.

    Args:
        namespace (dict): A dict of variables that are available in every template loaded by the environment.
        search_path (str): A path to the directory that contains the templates. Can be relative or absolute.
            Relative paths are relative to the running `flow` directory.

    Example:
        Load a environment block:
        ```python
        from prefect_jinja import JinjaEnvironmentBlock
        block = JinjaEnvironmentBlock.load("BLOCK_NAME")
        ```
    """

    _block_type_name = "Jinja Environment"
    # _logo_url = ""

    namespace: Dict[str, Optional[str]] = Field(
        default_factory=dict,
        description="A dict of variables that are available in every template loaded by the environment.",
    )
    search_path: Optional[str] = Field(
        description="A path to the directory that contains the templates. Can be relative or absolute. Relative paths are relative to the running `flow` directory.",
    )

    def get_env(self) -> Environment:
        """
        Creates a Jinja Environment with a loader that searches for template files in the path provided by the
        `search_path` attribute and sets the global variables provided by the `namespace` attribute.

        Returns:
            JinjaEnvironment (Environment): A Jinja environment.

        Example:
            Gets a Jinja Environment.

            ```python
            from prefect import flow
            from prefect_jinja import jinja_render_from_template
            @flow
            def example_get_jinja_environment_flow():
                env_block = JinjaEnvironmentBlock(
                    search_path="templates", namespace={"sender_mail": "sender@test.com"}
                )
                return env_block.get_env()
            jinja_env = example_get_jinja_environment_flow()
            ```
        """
        loader = FileSystemLoader(self.search_path)
        env = Environment(
            loader=loader, autoescape=select_autoescape(), enable_async=True
        )
        if self.namespace is not None:
            env.globals = self.namespace.copy()

        return env
