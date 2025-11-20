# src/clients/books_client.py

import requests


class BooksClient:
    """
    Simple client for the FakeRestAPI Books endpoints.
    The goal is to have one place that knows how to call the API.
    """

    def __init__(self, base_url):
        # Store the base URL without a trailing slash
        self.base_url = base_url.rstrip("/")

    def _books_url(self):
        # Helper to build the base URL for all books operations
        return f"{self.base_url}/api/v1/Books"

    def list_books(self):
        """
        Get the full list of books.
        Basic GET request, no parameters.
        """
        return requests.get(self._books_url())

    def get_book(self, book_id):
        """
        Get a single book by id.
        Very simple GET with a path parameter.
        """
        url = f"{self._books_url()}/{book_id}"
        return requests.get(url)

    def create_book(self, payload):
        """
        Create a new book with a JSON payload.
        Assumes the API accepts a basic JSON body.
        """
        return requests.post(self._books_url(), json=payload)

    def update_book(self, book_id, payload):
        """
        Update an existing book by id.
        Sends the full JSON body to the API.
        """
        url = f"{self._books_url()}/{book_id}"
        return requests.put(url, json=payload)

    def delete_book(self, book_id):
        """
        Delete a book by id.
        Simple DELETE request.
        """
        url = f"{self._books_url()}/{book_id}"
        return requests.delete(url)
