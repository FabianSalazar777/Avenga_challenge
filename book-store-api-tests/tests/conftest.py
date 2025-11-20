# tests/conftest.py

import os
import random
import string
import pytest
import sys

# Ensure src is in the path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

from clients.books_client import BooksClient


@pytest.fixture(scope="session")
def base_url():
    return os.getenv("BASE_URL", "https://fakerestapi.azurewebsites.net")


@pytest.fixture(scope="session")
def books_client(base_url):
    return BooksClient(base_url)


def _random_string(size=8):
    return "".join(random.choice(string.ascii_letters) for _ in range(size))


@pytest.fixture
def new_book_payload():
    return {
        "id": 1,
        "title": f"Test Book {_random_string()}",
        "description": "Simple test description",
        "pageCount": 100,
        "excerpt": "Sample excerpt for tests",
        "publishDate": "2025-11-19T00:00:00Z",
    }
