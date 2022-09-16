"""Tasks for rendering Jinja Templates."""
from typing import Dict, Union

from jinja2 import Template
from prefect import task
from prefect.context import get_run_context, FlowRunContext, TaskRunContext

from prefect_jinja.blocks import JinjaEnvironmentBlock


def _get_template_context(context: Union[FlowRunContext, TaskRunContext]) -> Dict:
    """
    Transforms the context of a running task into a dict to make it available in the template.

    Args:
        context: The current run context of a task or flow function.

    Returns:
        A dict of `TaskRunContext`.
    """
    return {"context": context.task_run.dict()}


@task
async def jinja_render_from_template(name: str, jinja_environment: JinjaEnvironmentBlock, **kwargs) -> str:
    """
    Task that performs the rendering of a template file based on settings of a `Jinja Environment` block.

    !!! note Context
        The context of a task will be available in the template via `context` keyword.

    Args:
        name: Name of template file to render.
        jinja_environment: A Jinja Environment block.
        **kwargs (dict): Keywords that will be available as variables in the template.

    Raises:
        TemplateNotFound: If the template file does not exist.
        TemplateSyntaxError: If there is a problem with the template.

    Returns:
        A string containing the rendered template.

    Examples:
        Render a welcome template file inside `templates` folder with `company_name` as block variable and `username`
        as keyword:
        ```python
        @flow
        def send_welcome_flow(username: str):
            jinja_environment = JinjaEnvironmentBlock(
                search_path="templates",
                namespace={
                    "company_name": "Acme",
                }
            )
            return jinja_render_from_template(
                "welcome.html",
                jinja_environment,
                username=username
            )
        print(send_welcome_flow(username="Neymar"))
        ```
    """
    context = get_run_context()
    jinja_env = jinja_environment.get_env()

    template = jinja_env.get_template(name, globals=_get_template_context(context))

    return await template.render_async(**kwargs)


@task
async def jinja_render_from_string(template_string: str, **kwargs) -> str:
    """
    Task that performs the rendering of a string.

    !!! note Context
        The context of a task will be available in the template via `context` keyword.

    Args:
        template_string: A string representing a template.
        **kwargs (dict): Keywords that will be available as variables in the template.

    Raises:
        TemplateSyntaxError: If there is a problem with the template.

    Returns:
        A string containing the rendered template.

    Examples:
        Render a hello with username:
        ```python
        @flow
        def send_hello_flow(username: str):
            return jinja_render_from_string("Hello, {{name}}!", username=username)
        print(send_hello_flow(username="Robinho"))
        ```
    """
    context = get_run_context()

    template = Template(template_string, enable_async=True)
    template.globals = _get_template_context(context)

    return await template.render_async(**kwargs)
