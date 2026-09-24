name: Python CI

on:
  push:
    branches:
      - main
      - master

  pull_request:
    branches:
      - main
      - master

  workflow_dispatch:

jobs:
  ci:
    runs-on: ubuntu-latest

    permissions:
      contents: read

    steps:
      # 1. Repository checkout
      - name: Checkout repository
        uses: actions/checkout@v4

      # 2. Setup Python
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.12"
          cache: pip

      # 3. Install dependencies
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements-dev.txt

      # 4. Run Flake8
      - name: Flake8 linting
        run: flake8 src tests scripts

      # 5. Check Black formatting
      - name: Black formatting check
        run: black --check src tests scripts

      # 6. Run tests with coverage
      - name: Run unit tests with coverage
        run: |
          pytest \
            --cov=src \
            --cov-report=term-missing \
            --cov-report=xml:coverage.xml \
            --cov-report=html:htmlcov \
            --cov-fail-under=90

      # 7. Run Bandit security scan
      - name: Bandit security scan
        run: bandit -r src scripts -x tests

      # 8. Check dependency vulnerabilities
      - name: Dependency vulnerability scan
        run: pip-audit

      # 9. Upload coverage report
      - name: Upload coverage report
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: coverage-report
          path: |
            coverage.xml
            htmlcov/
          if-no-files-found: ignore

      # 10. Send CI result by email
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