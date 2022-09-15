"""Tasks for interacting with Jinja"""
from typing import Dict

from jinja2 import Template
from prefect import task
from prefect.context import get_run_context

from prefect_jinja.blocks import JinjaEnvironmentBlock


def get_template_context(context) -> Dict:
    return {
        "context": {
            "start_time": context.start_time,
        }
    }


@task
async def jinja_render_from_template(name: str, jinja_environment: JinjaEnvironmentBlock, **kwargs) -> str:
    """
    Task that performs the rendering of a template file.

    Args:
        name (str): Name of template to load.
        jinja_environment (JinjaEnvironmentBlock): Block.
        **kwargs: Other arguments that will be passed to the model as variables.

    Raises:
        TemplateNotFound: If the template does not exist.
        TemplateSyntaxError: If there is a problem with the template.

    Returns:
        str: The rendered template as a string.

    Examples:
        Render a welcome template to send via email (see the 'prefect-email' collection):
        ```python
        from prefect import flow
        from prefect_email import EmailServerCredentials, email_send_message
        from prefect_jinja import jinja_render_from_template

        @flow
        def example_send_welcome_email_flow():
            env_block = JinjaEnvironmentBlock(search_path="templates", namespace={"sender_mail": "sender@test.com"})
            email_body = jinja_render_from_template("welcome.html", env_block, name="Test", email="test@test.com")
            email_server_credentials = EmailServerCredentials(
                username="your_email_address@gmail.com",
                password="MUST_be_an_app_password_here!",
            )
            subject = email_send_message(
                email_server_credentials=email_server_credentials,
                subject="Example Flow Notification using Gmail",
                msg=email_body,
                email_to="sender@test.com",
            )
        example_send_welcome_email_flow()
        ```

    """
    jinja_env = jinja_environment.get_env()
    template = jinja_env.get_template(name, globals=get_template_context(get_run_context()))

    return await template.render_async(**kwargs)


@task
async def jinja_render_from_string(template_string: str, **kwargs) -> str:
    template = Template(template_string, enable_async=True)
    template.globals = get_template_context(get_run_context())

    return await template.render_async(**kwargs)
