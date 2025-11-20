# Book Store API Tests

[![Python](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/)
[![pytest](https://img.shields.io/badge/tested%20with-pytest-green.svg)](https://docs.pytest.org/en/stable/)

Automated test suite for the Book Store API using Python and pytest.

## Summary

This repository contains API tests that validate the behavior of a Book Store service, covering both happy-path and negative scenarios. A simple client wrapper is available in `src/clients/books_client.py`, and test cases are located under `tests/`.

## Prerequisites

- Python 3.8 or newer
- pip
- virtual environment tool such as `venv`

## Installation

1. Create and activate a virtual environment (recommended):
   ```sh
   python3 -m venv venv
   source venv/bin/activate   # Mac/Linux
   ```
2. Install dependencies:
   ```sh
   python3 -m pip install --upgrade pip
   pip3 install -r book-store-api-tests/requirements.txt
   ```

## Project Structure

- `src/client/book_client.py` – simple client wrapper for API requests
- `test/conftest.py` – pytest fixtures and configuration
- `test/test_book_happy_path.py` – positive test cases
- `test/test_book_negative.py` – negative/edge cases
- `pytest.ini` – pytest configuration
- `Jenkinsfile` – CI pipeline configuration

## Configuration

Check `test/conftest.py` for configuration options (such as base URL). You can also override environment variables depending on your CI/CD environment.

## Running Tests Locally

- It’s important to be in the terminal inside the virtual environment and then run the following commands:
  ```sh
  mkdir -p reports
  export BASE_URL=https://fakerestapi.azurewebsites.net
  python3 -m pytest book-store-api-tests/tests \
                        --html=reports/report.html \
                        --self-contained-html \
                        --log-cli-level=INFO
  ```
- Once the report directory has been created, we only need to run the previously mentioned command:
```sh
  python3 -m pytest book-store-api-tests/tests \
                        --html=reports/report.html \
                        --self-contained-html \
                        --log-cli-level=INFO
  ```
## Report

The report must be opened in a web browser, and it is stored in the reports directory under the name report.html.”

## Continuous Integration

The included `Jenkinsfile` provides an example of how to run the tests in a Jenkins pipeline. 

### Exiting the Virtual Environment

Once you finish running your tests or working inside the virtual environment, you can exit it at any time by using:

```sh
deactivate
