"""This is an example blocks module"""

from prefect.blocks.core import Block
from pydantic import Field


class JinjaEnvironmentBlock(Block):
    """
    A sample block that holds a value.

    Args:
        value (str): The value to store.

    Example:
        Load a stored value:
        ```python
        from prefect_jinja import JinjaBlock
        block = JinjaBlock.load("BLOCK_NAME")
        ```
    """

    value: str = Field("The default value", description="The value to store")

    @classmethod
    def seed_value_for_example(cls):
        """
        Seeds the field, value, so the block can be loaded.
        """
        block = cls(value="A sample value")
        block.save("sample-block", overwrite=True)
