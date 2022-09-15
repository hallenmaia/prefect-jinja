"""A Jinja blocks module"""
from typing import Dict, Optional, Union

from jinja2 import Environment, FileSystemLoader, select_autoescape
from prefect.blocks.core import Block
from pydantic import Field


class JinjaEnvironmentBlock(Block):
    """
    Block to create a template environment.

    Instances of this class are used to store the configuration and global objects, and are used to load templates from
    the file system or other locations.

    Args:
        namespace (dict): A dict of variables that are available in every template loaded by the environment.
        search_path (str): A path to the directory that contains the templates. Can be relative or absolute. Relative
            paths are relative to the current working directory.

    Example:
        Load a environment config:
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
        default="templates",
        description="A path to the directory that contains the templates. Can be relative or absolute. Relative paths "
                    "are relative to the current working directory.",
    )

    def get_env(self) -> Environment:
        """
        Creates a template environment with a loader that looks up templates in the `search_path`.

        It also store `namespace` as variables that should be available without needing to pass them to
        :py:func:`~prefect_jinja.tasks.jinja_render_from_template` task.

        Returns:
            Environment: A Jinja environment.

        Example:
            Gets a Jinja environment.

            ```python
            from prefect import flow
            from prefect_jinja import jinja_render_from_template
            @flow
            def example_get_jinja_environment_flow():
                env_block = JinjaEnvironmentBlock(
                    search_path="templates", namespace={"sender_mail": "sender@test.com"}
                )
                env = env_block.get_env()
                return env
            example_get_jinja_environment_flow()
            ```
        """
        loader = FileSystemLoader(self.search_path)
        env = Environment(
            loader=loader, autoescape=select_autoescape(), enable_async=True
        )
        if self.namespace is not None:
            env.globals = self.namespace.copy()

        return env
