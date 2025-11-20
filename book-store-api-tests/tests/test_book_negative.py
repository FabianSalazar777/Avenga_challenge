from http import HTTPStatus
import logging

logger = logging.getLogger(__name__)


class TestBooksNegative:
    """
    Tests that cover simple negative or error scenarios.
    The goal is to show how the API behaves with bad input or missing data.
    """

    def test_get_non_existing_book(self, books_client):
        """
        Try to get a book with a very large id that should not exist.
        We expect an error status code from the API.
        """
        non_existing_id = 99999999
        logger.info(f"Requesting non-existing book id={non_existing_id}")

        response = books_client.get_book(non_existing_id)
        logger.info(f"Get non-existing book status code: {response.status_code}")
        logger.info(f"Response body: {response.text}")

        assert response.status_code in (HTTPStatus.NOT_FOUND, HTTPStatus.BAD_REQUEST)

    def test_delete_non_existing_book(self, books_client):
        """
        Try to delete a book that does not exist.
        Different APIs return different codes, so we allow a small range.
        """
        non_existing_id = 99999999
        logger.info(f"Attempting to delete non-existing book id={non_existing_id}")

        response = books_client.delete_book(non_existing_id)
        logger.info(f"Delete non-existing book status code: {response.status_code}")
        logger.info(f"Response body: {response.text}")

        assert response.status_code in (
            HTTPStatus.NOT_FOUND,
            HTTPStatus.OK,
            HTTPStatus.BAD_REQUEST,
        )

    def test_create_book_with_invalid_payload(self, books_client):
        """
        Send an invalid payload to the API.
        Here we send a wrong type for pageCount on purpose.
        """
        invalid_payload = {
            "pageCount": "not-a-number",
        }

        logger.info("Sending invalid payload to create a book")
        logger.info(f"Payload: {invalid_payload}")

        response = books_client.create_book(invalid_payload)
        logger.info(f"Create invalid book status code: {response.status_code}")
        logger.info(f"Response body: {response.text}")

        # We only check that the API does not consider this a successful creation
        assert response.status_code not in (HTTPStatus.OK, HTTPStatus.CREATED)
