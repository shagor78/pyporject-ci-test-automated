# CI Code Quality & Security Tools Explained

This guide explains three common tools used in a Python CI pipeline:

- Flake8
- Black
- Bandit

They solve different problems and are often used together in GitHub Actions.

---

## 1. Flake8 — Python Linting and Code Quality

Flake8 is a **Python linter**. It checks your Python code for style problems, syntax-related issues, and common programming mistakes.

A simple way to describe it is:

> **Flake8 asks: "Is this Python code written cleanly and according to common standards?"**

### What Flake8 checks

Flake8 can detect things such as:

- Unused imports
- Undefined variables
- Bad indentation
- Lines that are too long
- Extra whitespace
- Missing whitespace
- Some common Python coding mistakes
- PEP 8 style violations

### Example

Suppose you write:

```python
import os

name="Nure"
print(  name )
```

Flake8 may report formatting and style issues such as missing spaces around `=` and unnecessary whitespace.

Another example:

```python
import os

print("Hello")
```

If `os` is never used, Flake8 may report:

```text
F401 'os' imported but unused
```

### Install Flake8

```bash
pip install flake8
```

### Run Flake8

Scan the current project:

```bash
flake8 .
```

Or scan specific folders:

```bash
flake8 src tests
```

### Example GitHub Actions step

```yaml
- name: Flake8 linting
  run: flake8 src tests
```

If Flake8 finds violations that are treated as errors, the command exits with a non-zero status and the CI job fails.

### Flake8 in one sentence

> **Flake8 checks whether your Python code follows quality and style rules.**

---

## 2. Black — Automatic Python Code Formatter

Black is a **Python code formatter**.

Unlike Flake8, which reports style problems, Black can automatically rewrite the code into a consistent format.

A simple way to describe it is:

> **Black asks: "Is this Python code formatted exactly the way the project expects?"**

### What Black does

Black automatically handles formatting such as:

- Spacing
- Line breaks
- Indentation
- Long expressions
- Function-call formatting
- Lists and dictionaries
- Quotes and general code layout

The goal is to make formatting consistent across the entire development team.

### Example

Before Black:

```python
def add(a,b):
    return a+b
```

After Black:

```python
def add(a, b):
    return a + b
```

Another example:

Before:

```python
users = [{"name":"Nure","role":"Engineer"},{"name":"Aman","role":"Developer"}]
```

Black may rewrite it into a more readable form:

```python
users = [
    {"name": "Nure", "role": "Engineer"},
    {"name": "Aman", "role": "Developer"},
]
```

### Install Black

```bash
pip install black
```

### Automatically format code

```bash
black .
```

This changes the files.

### Check formatting without changing files

In CI, you usually use:

```bash
black --check .
```

This checks whether the code is already properly formatted.

If formatting is incorrect, Black returns a failure status and the CI pipeline can fail.

### Example GitHub Actions step

```yaml
- name: Black formatting check
  run: black --check src tests
```

### Why use `--check` in CI?

You usually do not want the CI server silently modifying source code.

Instead, CI checks the formatting and tells developers to fix it before merging.

Developers can run:

```bash
black .
```

locally to automatically fix formatting.

### Black in one sentence

> **Black makes Python formatting consistent and removes formatting debates from the team.**

---

## 3. Bandit — Python Security Scan

Bandit is a **static security scanner for Python code**.

It examines Python source code and looks for patterns that may introduce security vulnerabilities.

A simple way to describe it is:

> **Bandit asks: "Is this Python code potentially dangerous or insecure?"**

### What Bandit checks

Bandit can detect security risks such as:

- Hard-coded passwords
- Dangerous use of `eval()`
- Dangerous use of `exec()`
- Unsafe subprocess execution
- `shell=True`
- Weak cryptographic algorithms
- Insecure temporary files
- Unsafe SSL/TLS configuration
- Some SQL-related security patterns
- Security-sensitive Python functions

### Example: hard-coded password

```python
password = "admin123"
```

Hard-coded credentials are dangerous because they can accidentally be committed to GitHub.

Bandit may flag this kind of pattern.

### Example: dangerous `eval()`

```python
user_input = input("Enter expression: ")
result = eval(user_input)
```

`eval()` can execute arbitrary Python code.

If an attacker controls the input, this can become a serious vulnerability.

### Example: command injection risk

```python
import subprocess

subprocess.run(
    "ping " + user_input,
    shell=True,
)
```

Using user-controlled input together with:

```python
shell=True
```

can lead to command injection.

Bandit may report something similar to:

```text
Issue: [B602:subprocess_popen_with_shell_equals_true]
Severity: High
Confidence: High
```

### Install Bandit

```bash
pip install bandit
```

### Run Bandit

Scan the current project:

```bash
bandit -r .
```

Scan only application code:

```bash
bandit -r src
```

Scan multiple directories:

```bash
bandit -r src scripts
```

Exclude tests:

```bash
bandit -r src scripts -x tests
```

### Understanding this command

```bash
bandit -r src scripts -x tests
```

means:

- `bandit` — run Bandit
- `-r` — scan recursively
- `src scripts` — scan these directories
- `-x tests` — exclude the tests directory

### Example GitHub Actions step

```yaml
- name: Bandit security scan
  run: bandit -r src scripts -x tests
```

If Bandit finds security issues that match its configured failure criteria, the CI pipeline can fail.

### Bandit in one sentence

> **Bandit is a security linter for Python that looks for potentially unsafe coding patterns.**

---

# Flake8 vs Black vs Bandit

These tools may all scan Python files, but they have different responsibilities.

| Tool | Main Purpose | Main Question |
|---|---|---|
| Flake8 | Linting and code quality | Is the code clean and following coding standards? |
| Black | Code formatting | Is the code formatted consistently? |
| Bandit | Security scanning | Is the code using potentially insecure patterns? |

For example:

```python
import subprocess

name="Nure"

subprocess.run("echo "+name,shell=True)
```

Different tools may react for different reasons.

### Flake8

Flake8 may complain about:

```python
name="Nure"
```

because spacing does not follow normal Python style.

It may also detect unused imports or other quality issues.

### Black

Black would automatically reformat it:

```python
name = "Nure"

subprocess.run("echo " + name, shell=True)
```

Black makes it look consistent, but it does **not** mean the code is secure.

### Bandit

Bandit may complain about:

```python
shell=True
```

because this can become a command injection risk.

This is why all three tools are useful.

---

# How They Fit Into CI

A typical Python CI pipeline may look like this:

```text
Developer Push / Pull Request
              |
              v
       GitHub Actions
              |
              v
        Flake8
   Code quality check
              |
              v
          Black
     Formatting check
              |
              v
          Pytest
       Unit testing
              |
              v
          Bandit
      Security scanning
              |
              v
          Result
        /        \
     PASS        FAIL
      |            |
      v            v
   CI Success   CI Failure
```

Each tool answers a different question:

```text
Flake8
"Is my code clean?"

Black
"Is my code formatted consistently?"

Pytest
"Does my code work?"

Bandit
"Is my code potentially insecure?"
```

---

# Example GitHub Actions Configuration

A basic CI workflow could contain:

```yaml
- name: Flake8 linting
  run: flake8 src tests scripts

- name: Black formatting check
  run: black --check src tests scripts

- name: Run unit tests
  run: pytest

- name: Bandit security scan
  run: bandit -r src scripts -x tests
```

The pipeline runs each quality gate before allowing the build to be considered successful.

---

# Recommended Developer Workflow

Before pushing code to GitHub, developers can run:

```bash
black .
```

Then:

```bash
flake8 .
```

Then:

```bash
pytest
```

Then:

```bash
bandit -r .
```

A useful development workflow is:

```text
Write Code
    |
    v
Black
Auto-format code
    |
    v
Flake8
Check code quality
    |
    v
Pytest
Check functionality
    |
    v
Bandit
Check security
    |
    v
Git Push
    |
    v
GitHub Actions repeats the checks
```

---

# Easy Way to Remember

Think about the tools like members of a software engineering team.

### Black — The Formatter

Black says:

> "I'll make everyone's Python code look consistent."

### Flake8 — The Code Reviewer

Flake8 says:

> "I'll check whether the code follows good Python coding practices."

### Bandit — The Security Engineer

Bandit says:

> "I'll look for code that could create a security vulnerability."

### Pytest — The Tester

Pytest says:

> "I'll verify whether the application behaves as expected."

Together they provide:

```text
Formatting
    +
Code Quality
    +
Testing
    +
Security
    =
Better CI Pipeline
```

---

# Important Note

Passing Flake8, Black, and Bandit does **not** guarantee that an application is bug-free or completely secure.

They are automated quality gates that help catch common issues early.

A production security strategy may also include:

- Dependency vulnerability scanning
- Secret scanning
- SAST tools
- Container image scanning
- DAST
- Infrastructure scanning
- Code review
- Penetration testing

For Python dependency vulnerabilities, a commonly used additional tool is:

```bash
pip-audit
```

The distinction is:

```text
Bandit
   |
   +--> Scans your Python source code

pip-audit
   |
   +--> Scans installed Python dependencies for known vulnerabilities
```

Together, they provide stronger coverage than either tool alone.




# Purpose of the file: `.flake8`
The .flake8 file is the configuration file for Flake8. It lets you define your project’s linting rules once, instead of typing options every time you run: `flake8 .`

`max-line-length = 88` means Flake8 allows a Python line to be up to 88 characters before reporting a line-length violation. That value is commonly used when the project also uses Black, because Black's default line length is 88.

For example, without this setting, Flake8 may complain about a line like:

`message = "This is a relatively long line that may exceed Flake8's normal default."`

because Flake8's traditional default limit is 79 characters.


# Purpose of the file: `pyproject.toml`
`pyproject.toml` is a central configuration file for Python projects. Modern Python tools use it to store project metadata and tool settings in one place.

Instead of having separate configuration files for every tool, you can put settings for tools like Black, Pytest, Ruff, mypy, coverage, build systems, and package metadata inside pyproject.toml.

For example, in the project I gave you:

```bash
[tool.black]
line-length = 88
target-version = ["py312"]

[tool.pytest.ini_options]
testpaths = ["tests"]
pythonpath = ["."]
```

### The first section configures Black.

### The second section configures Pytest.

`testpaths = ["tests"]` tells Pytest: Look for tests inside the tests/ directory


## Conceptually:

```bash
pyproject.toml
     |
     +--> Black settings
     |
     +--> Pytest settings
     |
     +--> Ruff settings
     |
     +--> mypy settings
     |
     +--> package/build settings
     |
     +--> other Python tooling
```

Many modern Python tools support pyproject.toml, which is why it has become the preferred place for configuration. `pyproject.toml` is the central settings file for a modern Python project.



# GitHub Actions `ci.yml` Explained

This guide explains the purpose of the GitHub Actions CI workflow used in this Python project.

The workflow file is located at:

```text
.github/workflows/ci.yml
```

GitHub automatically detects YAML workflow files inside:

```text
.github/workflows/
```

and runs them based on the events defined in the workflow.

---

# Complete `ci.yml`

```yaml
name: Python CI

on:
  push:
    branches:
      - main
  pull_request:
    branches:
      - main
  workflow_dispatch:

jobs:
  ci:
    runs-on: ubuntu-latest

    permissions:
      contents: read

    steps:
      - name: Checkout repository
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.12"
          cache: pip

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements-dev.txt

      - name: Flake8 linting
        run: flake8 src tests scripts

      - name: Black formatting check
        run: black --check src tests scripts

      - name: Run unit tests with coverage
        run: |
          pytest \
            --cov=src \
            --cov-report=term-missing \
            --cov-report=xml:coverage.xml \
            --cov-report=html:htmlcov \
            --cov-fail-under=90

      - name: Bandit security scan
        run: bandit -r src scripts -x tests

      - name: Dependency vulnerability scan
        run: pip-audit

      - name: Upload coverage report
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: coverage-report
          path: |
            coverage.xml
            htmlcov/
          if-no-files-found: ignore

      - name: Send CI email
        if: always()
        continue-on-error: true
        env:
          SMTP_SERVER: ${{ secrets.SMTP_SERVER }}
          SMTP_PORT: ${{ secrets.SMTP_PORT }}
          SMTP_USERNAME: ${{ secrets.SMTP_USERNAME }}
          SMTP_PASSWORD: ${{ secrets.SMTP_PASSWORD }}
          CI_EMAIL_RECIPIENT: ${{ secrets.CI_EMAIL_RECIPIENT }}
          CI_STATUS: ${{ job.status }}
        run: python scripts/send_ci_email.py
```

---

# What This CI Pipeline Does

The workflow performs the following steps:

```text
Developer Push / Pull Request
            |
            v
     GitHub Actions
            |
            v
   Checkout Repository
            |
            v
     Set Up Python
            |
            v
 Install Dependencies
            |
            v
        Flake8
   Code Quality Check
            |
            v
         Black
   Formatting Check
            |
            v
         Pytest
  Unit Tests + Coverage
            |
            v
         Bandit
    Security Scan
            |
            v
       pip-audit
 Dependency Security Scan
            |
            v
  Upload Coverage Report
            |
            v
     Send CI Email
```

---

# 1. Workflow Name

```yaml
name: Python CI
```

This gives the workflow a readable name.

Inside the GitHub Actions interface, you will see:

```text
Python CI
```

instead of only the filename.

---

# 2. Workflow Triggers

```yaml
on:
  push:
    branches:
      - main
  pull_request:
    branches:
      - main
  workflow_dispatch:
```

The `on:` section defines when GitHub Actions should run the workflow.

## Run on Push

```yaml
push:
  branches:
    - main
```

This means:

> Run this CI workflow whenever code is pushed to the `main` branch.

For example:

```bash
git push origin main
```

will trigger the workflow.

---

## Run on Pull Request

```yaml
pull_request:
  branches:
    - main
```

This means:

> Run the CI workflow when someone opens or updates a Pull Request targeting the `main` branch.

Example:

```text
feature/login
      |
      | Pull Request
      v
    main
```

Before merging, GitHub Actions can verify that the code passes:

- linting
- formatting
- unit tests
- security checks

---

## Manual Run

```yaml
workflow_dispatch:
```

This enables a **Run workflow** button in GitHub Actions.

It allows you to manually start the CI pipeline without making a new commit.

This is useful for:

- testing the CI pipeline
- demonstrations
- classroom labs
- rerunning checks manually

---

# 3. Jobs

```yaml
jobs:
  ci:
```

A GitHub Actions workflow contains one or more **jobs**.

In this example, the job is named:

```text
ci
```

A job contains a sequence of steps.

---

# 4. Runner

```yaml
runs-on: ubuntu-latest
```

This tells GitHub:

> Create a temporary Ubuntu virtual machine and run the CI job there.

Conceptually:

```text
GitHub
   |
   v
Temporary Ubuntu VM
   |
   v
Run CI Steps
   |
   v
Destroy VM
```

The virtual machine is created for the workflow and removed after the job finishes.

---

# 5. Permissions

```yaml
permissions:
  contents: read
```

This follows the principle of **least privilege**.

The workflow only needs permission to read repository contents.

It does not need permission to modify code.

This is generally safer than giving workflows unnecessary permissions.

---

# 6. Steps

```yaml
steps:
```

The `steps` section contains the commands and GitHub Actions that run inside the job.

They normally execute from top to bottom.

If a normal step fails, later normal steps usually do not run unless special conditions are used.

---

# 7. Checkout Repository

```yaml
- name: Checkout repository
  uses: actions/checkout@v4
```

When GitHub creates the runner, your repository code is not automatically available in the working directory.

`actions/checkout` downloads the repository into the runner.

Conceptually:

```text
GitHub Repository
       |
       v
actions/checkout
       |
       v
Ubuntu Runner
       |
       v
Project files are available
```

After this step, GitHub Actions can access files such as:

```text
src/
tests/
scripts/
requirements-dev.txt
pyproject.toml
.flake8
```

---

# 8. Set Up Python

```yaml
- name: Set up Python
  uses: actions/setup-python@v5
  with:
    python-version: "3.12"
    cache: pip
```

This installs and configures Python 3.12 on the GitHub Actions runner.

## Python Version

```yaml
python-version: "3.12"
```

This makes the CI environment use Python 3.12.

This is useful because your local environment and CI environment should ideally use the same Python version.

---

## pip Cache

```yaml
cache: pip
```

This enables dependency caching.

Without caching:

```text
Workflow Run 1
Download dependencies

Workflow Run 2
Download dependencies again

Workflow Run 3
Download dependencies again
```

With caching:

```text
Workflow Run 1
Download dependencies
        |
        v
      Cache

Workflow Run 2
Reuse cached packages
```

This can make repeated CI runs faster.

---

# 9. Install Dependencies

```yaml
- name: Install dependencies
  run: |
    python -m pip install --upgrade pip
    pip install -r requirements-dev.txt
```

This step installs the tools required by the CI pipeline.

The first command:

```bash
python -m pip install --upgrade pip
```

updates `pip`.

The second command:

```bash
pip install -r requirements-dev.txt
```

installs dependencies listed in:

```text
requirements-dev.txt
```

For example:

```text
pytest
pytest-cov
flake8
black
bandit
pip-audit
```

---

# 10. Flake8 Linting

```yaml
- name: Flake8 linting
  run: flake8 src tests scripts
```

Flake8 checks Python code quality and style.

It scans:

```text
src/
tests/
scripts/
```

Flake8 looks for problems such as:

- unused imports
- undefined variables
- bad indentation
- whitespace issues
- line-length problems
- PEP 8 violations

A simple way to remember Flake8 is:

> **Flake8 asks: "Is this Python code written cleanly?"**

If Flake8 finds violations that cause a non-zero exit code, the CI job fails.

---

# 11. Black Formatting Check

```yaml
- name: Black formatting check
  run: black --check src tests scripts
```

Black is a Python formatter.

The important option is:

```bash
--check
```

It means:

> Check whether the code is correctly formatted, but do not modify any files.

This is ideal for CI.

If code is not properly formatted, Black fails the step.

For example:

```python
def add(a,b):
    return a+b
```

Black expects something like:

```python
def add(a, b):
    return a + b
```

A simple way to remember Black is:

> **Black asks: "Is this code formatted consistently?"**

---

# 12. Unit Tests and Coverage

```yaml
- name: Run unit tests with coverage
  run: |
    pytest \
      --cov=src \
      --cov-report=term-missing \
      --cov-report=xml:coverage.xml \
      --cov-report=html:htmlcov \
      --cov-fail-under=90
```

This step runs your automated unit tests using Pytest.

It also measures test coverage.

---

## Run Tests

```bash
pytest
```

Pytest automatically discovers and runs test files.

For example:

```text
tests/test_calculator.py
```

---

## Measure Coverage

```bash
--cov=src
```

This tells Pytest:

> Measure how much code inside `src/` is executed by the tests.

For example:

```text
src/calculator.py
100% covered
```

or:

```text
src/calculator.py
72% covered
```

---

## Show Missing Lines

```bash
--cov-report=term-missing
```

This prints coverage information in the terminal and shows lines not covered by tests.

Example:

```text
Name                 Stmts   Miss  Cover   Missing
--------------------------------------------------
src/calculator.py       12      2    83%   14-15
```

---

## Generate XML Coverage Report

```bash
--cov-report=xml:coverage.xml
```

This creates:

```text
coverage.xml
```

XML coverage reports are useful for:

- CI integrations
- quality platforms
- reporting tools
- automated processing

---

## Generate HTML Coverage Report

```bash
--cov-report=html:htmlcov
```

This creates:

```text
htmlcov/
```

Inside it, you get an HTML report that you can open in a browser.

Example:

```text
htmlcov/index.html
```

The report visually shows:

- covered lines
- missed lines
- percentage coverage

---

## Minimum Coverage Threshold

```bash
--cov-fail-under=90
```

This means:

> Fail the CI pipeline if overall test coverage is below 90%.

Example:

```text
Coverage = 96%
CI passes
```

but:

```text
Coverage = 84%
CI fails
```

This makes test coverage a CI quality gate.

---

# 13. Bandit Security Scan

```yaml
- name: Bandit security scan
  run: bandit -r src scripts -x tests
```

Bandit performs static security analysis of Python source code.

It searches for potentially unsafe patterns.

Examples include:

- `eval()`
- hard-coded passwords
- unsafe `subprocess` usage
- `shell=True`
- weak cryptography
- insecure temporary files

A simple way to remember Bandit is:

> **Bandit asks: "Is this Python code potentially insecure?"**

---

## Understanding the Command

```bash
bandit -r src scripts -x tests
```

means:

```text
bandit
    Run Bandit

-r
    Scan recursively

src scripts
    Scan these directories

-x tests
    Exclude the tests directory
```

---

# 14. Dependency Vulnerability Scan

```yaml
- name: Dependency vulnerability scan
  run: pip-audit
```

`pip-audit` checks installed Python packages for known vulnerabilities.

This is different from Bandit.

```text
Bandit
   |
   +--> Scans your Python source code

pip-audit
   |
   +--> Scans third-party Python dependencies
```

For example, suppose your project installs:

```text
requests
flask
django
urllib3
```

`pip-audit` checks whether installed versions are associated with known published vulnerabilities.

A simple way to remember it is:

> **pip-audit asks: "Do any of my Python dependencies have known vulnerabilities?"**

---

# 15. Upload Coverage Report

```yaml
- name: Upload coverage report
  if: always()
  uses: actions/upload-artifact@v4
  with:
    name: coverage-report
    path: |
      coverage.xml
      htmlcov/
    if-no-files-found: ignore
```

This uploads generated coverage reports to GitHub Actions as an artifact.

The uploaded artifact is named:

```text
coverage-report
```

It contains:

```text
coverage.xml
htmlcov/
```

You can download the artifact from the GitHub Actions workflow run.

---

## Why `if: always()`?

```yaml
if: always()
```

means:

> Try to run this step even if a previous CI step failed.

Without it:

```text
Pytest fails
    |
    v
Later normal steps may be skipped
```

With:

```yaml
if: always()
```

GitHub still attempts to run the coverage upload step.

---

## Ignore Missing Files

```yaml
if-no-files-found: ignore
```

If coverage files do not exist, GitHub does not fail the workflow just because the artifact files are missing.

For example, if Pytest failed before generating HTML coverage:

```text
htmlcov/
```

may not exist.

This setting prevents the artifact step itself from causing another failure.

---

# 16. Send CI Email

```yaml
- name: Send CI email
  if: always()
  continue-on-error: true
  env:
    SMTP_SERVER: ${{ secrets.SMTP_SERVER }}
    SMTP_PORT: ${{ secrets.SMTP_PORT }}
    SMTP_USERNAME: ${{ secrets.SMTP_USERNAME }}
    SMTP_PASSWORD: ${{ secrets.SMTP_PASSWORD }}
    CI_EMAIL_RECIPIENT: ${{ secrets.CI_EMAIL_RECIPIENT }}
    CI_STATUS: ${{ job.status }}
  run: python scripts/send_ci_email.py
```

This step sends a success or failure email after the CI job finishes.

---

# 17. Why Email Uses `if: always()`

```yaml
if: always()
```

is especially important for notifications.

Suppose the workflow is:

```text
Flake8   PASS
Black    PASS
Pytest   FAIL
Bandit   SKIPPED
Email    ?
```

Without:

```yaml
if: always()
```

the notification might never run.

With it:

```text
Flake8   PASS
Black    PASS
Pytest   FAIL
Email    RUNS
```

This allows the email script to notify the team that CI failed.

---

# 18. Why `continue-on-error: true`?

```yaml
continue-on-error: true
```

means:

> If the email notification itself fails, do not make the entire CI result fail because of the notification problem.

For example:

```text
All Tests PASS
       |
       v
Email SMTP Server Unavailable
```

Without `continue-on-error: true`, the workflow could appear failed even though the application checks passed.

With it:

```text
Application CI = PASS
Email notification = failed
Overall application quality result is not changed by the email issue
```

This is useful because notification infrastructure should not normally determine whether your code is valid.

---

# 19. GitHub Secrets

The email step uses values like:

```yaml
${{ secrets.SMTP_SERVER }}
```

These values come from GitHub Secrets.

Configure them at:

```text
Repository
   |
   v
Settings
   |
   v
Secrets and variables
   |
   v
Actions
   |
   v
New repository secret
```

Required secrets:

```text
SMTP_SERVER
SMTP_PORT
SMTP_USERNAME
SMTP_PASSWORD
CI_EMAIL_RECIPIENT
```

Example Gmail settings:

```text
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your-email@gmail.com
SMTP_PASSWORD=<Google App Password>
CI_EMAIL_RECIPIENT=team@example.com
```

Never hard-code passwords directly inside `ci.yml`.

Bad:

```yaml
SMTP_PASSWORD: mypassword123
```

Good:

```yaml
SMTP_PASSWORD: ${{ secrets.SMTP_PASSWORD }}
```

---

# 20. Job Status

```yaml
CI_STATUS: ${{ job.status }}
```

GitHub provides the current job status.

Possible values commonly include:

```text
success
failure
cancelled
```

The email script can use that value to decide whether to send:

```text
✅ CI Passed
```

or:

```text
❌ CI Failed
```

---

# 21. Run the Email Script

```yaml
run: python scripts/send_ci_email.py
```

This runs the Python email script.

The script reads the environment variables provided in:

```yaml
env:
```

and sends the notification using SMTP.

---

# 22. What Causes CI to Fail?

The workflow acts like a sequence of quality gates.

For example:

```text
Flake8
   |
   | PASS
   v
Black
   |
   | PASS
   v
Pytest
   |
   | PASS
   v
Coverage >= 90%
   |
   | PASS
   v
Bandit
   |
   | PASS
   v
pip-audit
   |
   | PASS
   v
CI SUCCESS
```

If an important quality check fails:

```text
Flake8
   |
   v
Black
   |
   v
Pytest
   |
   X FAIL
   |
   v
CI FAILURE
```

The notification step still runs because it uses:

```yaml
if: always()
```

---

# 23. Example Successful Pipeline

A successful GitHub Actions run may look like:

```text
Checkout repository              ✅
Set up Python                    ✅
Install dependencies             ✅
Flake8 linting                   ✅
Black formatting check           ✅
Run unit tests with coverage     ✅
Bandit security scan             ✅
Dependency vulnerability scan    ✅
Upload coverage report           ✅
Send CI email                    ✅
```

Result:

```text
✅ Python CI Passed
```

---

# 24. Example Failed Pipeline

Suppose a developer writes:

```python
def add(a, b):
    return a - b
```

but the test expects:

```python
assert add(2, 3) == 5
```

Pytest fails.

The workflow may look like:

```text
Checkout repository              ✅
Set up Python                    ✅
Install dependencies             ✅
Flake8 linting                   ✅
Black formatting check           ✅
Run unit tests with coverage     ❌
Upload coverage report           ✅
Send CI email                    ✅
```

Result:

```text
❌ Python CI Failed
```

The developer can then open the GitHub Actions logs and investigate the failing test.

---

# 25. Why Use All These Tools Together?

Each tool solves a different problem.

| Tool | Purpose | Main Question |
|---|---|---|
| Flake8 | Linting | Is the code clean? |
| Black | Formatting | Is the formatting consistent? |
| Pytest | Testing | Does the code work? |
| pytest-cov | Coverage | How much code is tested? |
| Bandit | Source security | Is the Python code potentially insecure? |
| pip-audit | Dependency security | Do dependencies have known vulnerabilities? |
| GitHub Actions | CI automation | Can all checks run automatically? |
| Email notification | Reporting | Did CI pass or fail? |

Together:

```text
Code Quality
      +
Formatting
      +
Testing
      +
Coverage
      +
Security
      +
Automation
      +
Notification
      =
Stronger CI Pipeline
```

---

# 26. How GitHub Actions Knows the Pipeline Failed

Most command-line tools return an **exit code**.

Conventionally:

```text
Exit Code 0
    =
Success
```

and:

```text
Non-zero Exit Code
    =
Failure
```

For example:

```bash
flake8 src
```

returns a non-zero exit code if blocking lint errors are found.

Similarly:

```bash
pytest
```

returns a non-zero exit code when tests fail.

GitHub Actions reads those exit codes.

Conceptually:

```text
Command
   |
   v
Exit Code
 /       \
0       Non-zero
|          |
v          v
PASS      FAIL
```

---

# 27. Running the Same Checks Locally

Developers should ideally run the same checks before pushing.

Install dependencies:

```bash
pip install -r requirements-dev.txt
```

Run formatting:

```bash
black .
```

Run linting:

```bash
flake8 src tests scripts
```

Run tests:

```bash
pytest
```

Run tests with coverage:

```bash
pytest --cov=src --cov-report=term-missing
```

Run Bandit:

```bash
bandit -r src scripts -x tests
```

Run dependency audit:

```bash
pip-audit
```

This reduces failed CI runs after pushing code.

---

# 28. CI vs CD

This workflow is mainly **CI**, or Continuous Integration.

It validates code automatically.

```text
Developer
   |
   v
Git Push
   |
   v
Continuous Integration
   |
   +--> Lint
   +--> Format check
   +--> Test
   +--> Security scan
```

A CD pipeline could continue after successful CI:

```text
CI Checks
   |
   v
Build Application
   |
   v
Build Docker Image
   |
   v
Push Image
   |
   v
Deploy to Dev
   |
   v
Deploy to Production
```

So this `ci.yml` is a good foundation that can later become part of a complete CI/CD pipeline.

---

# 29. Simple Explanation


```text
GitHub Actions = The Automation Engine

Flake8 = Code Reviewer

Black = Code Formatter

Pytest = Tester

pytest-cov = Test Coverage Inspector

Bandit = Python Security Engineer

pip-audit = Dependency Security Inspector

Email Script = Notification System
```

When a developer pushes code:

```text
Git Push
   |
   v
GitHub Actions
   |
   +--> Is the code clean?
   |
   +--> Is it formatted correctly?
   |
   +--> Does it work?
   |
   +--> Is enough code tested?
   |
   +--> Is our source code secure?
   |
   +--> Are dependencies vulnerable?
   |
   v
PASS / FAIL
   |
   v
Email Notification
```

That is the main purpose of this `ci.yml` workflow.
