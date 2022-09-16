# prefect-jinja

<p align="center">
    <a href="https://pypi.python.org/pypi/prefect-jinja/" alt="PyPI version">
        <img alt="PyPI" src="https://img.shields.io/pypi/v/prefect-jinja?color=0052FF&labelColor=090422"></a>
    <a href="https://github.com/hallenmaia/prefect-jinja/" alt="Stars">
        <img src="https://img.shields.io/github/stars/hallenmaia/prefect-jinja?color=0052FF&labelColor=090422" /></a>
    <a href="https://pepy.tech/badge/prefect-jinja/" alt="Downloads">
        <img src="https://img.shields.io/pypi/dm/prefect-jinja?color=0052FF&labelColor=090422" /></a>
    <a href="https://github.com/hallenmaia/prefect-jinja/pulse" alt="Activity">
        <img src="https://img.shields.io/github/commit-activity/m/hallenmaia/prefect-jinja?color=0052FF&labelColor=090422" /></a>
    <br>
    <a href="https://prefect-jinja-community.slack.com" alt="Slack">
        <img src="https://img.shields.io/badge/slack-join_community-red.svg?color=0052FF&labelColor=090422&logo=slack" /></a>
    <a href="https://discourse.prefect-jinja.io/" alt="Discourse">
        <img src="https://img.shields.io/badge/discourse-browse_forum-red.svg?color=0052FF&labelColor=090422&logo=discourse" /></a>
</p>

## Welcome!

`prefect-jinja` is a collection of pre-built Prefect tasks that can be used to quickly build Prefect flows to interact 
with [Jinja](https://jinja.palletsprojects.com).

## Getting Started

### Python setup

Requires an installation of Python 3.7+.

We recommend using a Python virtual environment manager such as pipenv, conda or virtualenv.

These tasks are designed to work with Prefect 2.0. For more information about how to use Prefect, please refer to the 
[Prefect documentation](https://docs.prefect.io/).

### Installation

Install `prefect-jinja` with `pip`:

```bash
pip install prefect-jinja
```

Then, register to [view the block](https://docs.prefect.io/ui/blocks/) on Prefect Cloud:

```bash
prefect block register -m prefect_jinja.blocks
```

!!! note "Load Block"
    To use the `load` method on Blocks, you must already have a block document 
    [saved through code](https://orion-docs.prefect.io/concepts/blocks/#saving-blocks) or 
    [saved through the UI](https://orion-docs.prefect.io/ui/blocks/).

### Write and run a flow

#### Render templates from a directory

Using the `JinjaEnvironmentBlock` block and the `jinja_render_from_template` function to render an HTML page.

!!! note "Remote storage"
    We recommend configuring [remote file storage](https://docs.prefect.io/concepts/storage/) for task execution with 
    `JinjaEnvironmentBlock` block and the `jinja_render_from_template` function. This ensures tasks have access to 
    templates files, particularly when accessing a instance outside the execution environment.

```python
from prefect import flow
from prefect_jinja import JinjaEnvironmentBlock, jinja_render_from_template

@flow
def example_jinja_render_from_template_flow(username: str):
    jinja_environment = JinjaEnvironmentBlock(
        search_path="templates", 
        namespace={
            "company_name": "Acme",
            "company_logo": "https://image.com",
        }
    )
    
    return jinja_render_from_template(
        "welcome.html", 
        jinja_environment, 
        username=username
    )
    
print(example_jinja_render_from_template_flow(username="Neymar"))
```

#### Render templates from a string

Using the `jinja_render_from_string` function to render a string.

```python
from prefect import flow
from prefect_jinja import jinja_render_from_string

@flow
def send_hello_flow(name: str):
    return jinja_render_from_string("Hello, {{name}}!", name=name)    

print(send_hello_flow(name="Robinho"))
```

## Resources

If you encounter any bugs while using `prefect-jinja`, feel free to open an issue in the 
[prefect-jinja](https://github.com/hallenmaia/prefect-jinja) repository.

If you have any questions or issues while using `prefect-jinja`, you can find help in either the 
[Prefect Discourse forum](https://discourse.prefect.io/) or the [Prefect Slack community](https://prefect.io/slack).

## Development

If you'd like to install a version of `prefect-jinja` for development, clone the repository and perform an editable 
install with `pip`:

```bash
git clone https://github.com/hallenmaia/prefect-jinja.git

cd prefect-jinja/

pip install -e ".[dev]"

# Install linting pre-commit hooks
pre-commit install
```
