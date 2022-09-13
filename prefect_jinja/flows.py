"""This is an example flows module"""
from prefect import flow

from prefect_jinja.blocks import JinjaBlock
from prefect_jinja.tasks import (
    goodbye_prefect_jinja,
    hello_prefect_jinja,
)


@flow
def hello_and_goodbye():
    """
    Sample flow that says hello and goodbye!
    """
    JinjaBlock.seed_value_for_example()
    block = JinjaBlock.load("sample-block")

    print(hello_prefect_jinja())
    print(f"The block's value: {block.value}")
    print(goodbye_prefect_jinja())
    return "Done"


if __name__ == "__main__":
    hello_and_goodbye()
