# Python GitHub Actions CI + Email Notifications

This sample project demonstrates a GitHub Actions CI pipeline that runs:

- Flake8 linting
- Black formatting validation
- Pytest unit tests
- Coverage reporting
- Bandit security scanning
- pip-audit dependency vulnerability scanning
- Email notification after the job completes
- Coverage report upload as a GitHub Actions artifact

## Project structure

```text
.
├── .github/
│   └── workflows/
│       └── ci.yml
├── scripts/
│   └── send_ci_email.py
├── src/
│   └── calculator.py
├── tests/
│   └── test_calculator.py
├── .flake8
├── .gitignore
├── pyproject.toml
├── requirements-dev.txt
└── README.md
```

## Run locally

Create a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements-dev.txt
```

Run all tests:

```bash
pytest
```

Run tests with coverage:

```bash
pytest --cov=src --cov-report=term-missing
```

Run Flake8:

```bash
flake8 src tests scripts
```

Run Black validation:

```bash
black --check src tests scripts
```

Run Bandit:

```bash
bandit -r src scripts -x tests
```

Run dependency security scan:

```bash
pip-audit
```

## GitHub Secrets required for email

In your GitHub repository go to:

**Settings → Secrets and variables → Actions → New repository secret**

Create these secrets:

```text
SMTP_SERVER
SMTP_PORT
SMTP_USERNAME
SMTP_PASSWORD
CI_EMAIL_RECIPIENT
```

### Gmail example

```text
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your-email@gmail.com
SMTP_PASSWORD=<Google App Password>
CI_EMAIL_RECIPIENT=team@example.com
```

Do not commit SMTP credentials to the repository.

For Gmail, use an App Password rather than your normal Google account password.

## How notification works

The workflow uses:

```yaml
if: always()
```

for the email step, which means the notification step runs whether the CI checks
pass or fail.

The script receives:

```yaml
CI_STATUS: ${{ job.status }}
```

and changes the email subject accordingly:

```text
✅ CI Passed — owner/repository
```

or:

```text
❌ CI Failed — owner/repository
```

The email also contains a direct link to the GitHub Actions workflow run.

## Coverage

The workflow requires at least 90% coverage:

```bash
--cov-fail-under=90
```

Change that value in `.github/workflows/ci.yml` if you want a different threshold.

## Try a failed pipeline

To create a failed scenario, temporarily change a test:

```python
def test_add():
    assert add(2, 3) == 100
```

Commit and push the change. Pytest will fail and the notification email should show
a failed CI status.

Then restore the correct assertion:

```python
assert add(2, 3) == 5
```

and push again to create a successful CI email notification.
