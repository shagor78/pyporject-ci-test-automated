import os
import smtplib
from email.message import EmailMessage


def required_env(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise RuntimeError(f"Required environment variable is missing: {name}")
    return value


def main() -> None:
    smtp_server = required_env("SMTP_SERVER")
    smtp_port = int(required_env("SMTP_PORT"))
    smtp_username = required_env("SMTP_USERNAME")
    smtp_password = required_env("SMTP_PASSWORD")
    recipient = required_env("CI_EMAIL_RECIPIENT")

    status = os.getenv("CI_STATUS", "unknown")
    repository = os.getenv("GITHUB_REPOSITORY", "unknown repository")
    workflow = os.getenv("GITHUB_WORKFLOW", "CI")
    branch = os.getenv("GITHUB_REF_NAME", "unknown")
    commit_sha = os.getenv("GITHUB_SHA", "unknown")
    actor = os.getenv("GITHUB_ACTOR", "unknown")
    server_url = os.getenv("GITHUB_SERVER_URL", "https://github.com")
    run_id = os.getenv("GITHUB_RUN_ID", "")

    run_url = (
        f"{server_url}/{repository}/actions/runs/{run_id}"
        if run_id
        else f"{server_url}/{repository}/actions"
    )

    if status == "success":
        subject = f"✅ CI Passed — {repository}"
        headline = "The GitHub Actions CI pipeline completed successfully. Ready for application build :)"
    else:
        subject = f"❌ CI Failed — {repository}"
        headline = f"The GitHub Actions CI pipeline finished with status: {status} :(."

    body = f"""\
{headline}

Repository: {repository}
Workflow:   {workflow}
Branch:     {branch}
Commit:     {commit_sha}
Triggered by: {actor}

Checks:
- Flake8 linting
- Black formatting check
- Pytest unit tests
- Coverage
- Bandit security scan
- pip-audit dependency scan

Workflow details:
{run_url}
"""

    message = EmailMessage()
    message["Subject"] = subject
    message["From"] = smtp_username
    message["To"] = recipient
    message.set_content(body)

    with smtplib.SMTP(smtp_server, smtp_port, timeout=30) as smtp:
        smtp.starttls()
        smtp.login(smtp_username, smtp_password)
        smtp.send_message(message)

    print(f"CI notification sent to {recipient}")


if __name__ == "__main__":
    main()
