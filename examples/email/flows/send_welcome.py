from prefect import flow
from prefect_email import EmailServerCredentials, email_send_message
from prefect_jinja import JinjaEnvironmentBlock, jinja_render_from_template


@flow
def send_welcome_flow(username: str, email_to: str):
    jinja_environment = JinjaEnvironmentBlock.load("email-templates")
    email_body = jinja_render_from_template(
        "welcome.html",
        jinja_environment,
        username=username
    )

    email_server_credentials = EmailServerCredentials.load("outgoing-mail-server")
    return email_send_message(
        email_server_credentials=email_server_credentials,
        subject="Welcome",
        msg=email_body,
        email_to=email_to,
    )


if __name__ == '__main__':
    result = send_welcome_flow(username="Jeronimo", email_to="jeronimo@example.com")
    print(result)


