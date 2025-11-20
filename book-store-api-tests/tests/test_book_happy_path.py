from http import HTTPStatus
import logging

logger = logging.getLogger(__name__)


class TestBooksHappyPath:
    """
    Tests that cover the normal (happy) flow of the Books API.
    The idea is to verify the standard CRUD operations.
    """

    def test_list_books_returns_200_and_list(self, books_client):
        """
        Basic test to check that listing books works
        and returns a list structure.
        """
        logger.info("Requesting list of books")
        response = books_client.list_books()

        logger.info(f"List books status code: {response.status_code}")
        assert response.status_code == HTTPStatus.OK

        data = response.json()
        logger.info(f"Number of books returned: {len(data)}")
        assert isinstance(data, list)

        # If there are items, do a very basic check on the first one
        if data:
            first = data[0]
            logger.info(f"First book sample: id={first.get('id')}, title={first.get('title')}")
            assert "id" in first
            assert "title" in first

    def test_get_existing_book_by_id(self, books_client):
        """
        First list books, then pick one id and get it again.
        This is a simple way to ensure the GET by id works.
        """
        logger.info("Listing books to obtain a valid id")
        list_response = books_client.list_books()
        logger.info(f"List books status code: {list_response.status_code}")
        assert list_response.status_code == HTTPStatus.OK

        books = list_response.json()
        logger.info(f"Books available: {len(books)}")
        assert len(books) > 0, "Expected at least one book in the API"

        book_id = books[0]["id"]
        logger.info(f"Retrieving book by id={book_id}")
        get_response = books_client.get_book(book_id)

        logger.info(f"Get book status code: {get_response.status_code}")
        assert get_response.status_code == HTTPStatus.OK

        book = get_response.json()
        logger.info(f"Received book id={book.get('id')}")
        assert book["id"] == book_id

    def test_create_book_and_get_it(self, books_client, new_book_payload):
        """
        Create a book and then get it again by id.
        Since the Fake API does NOT store data, we only validate status codes.
        """
        logger.info(f"Creating new book with title='{new_book_payload.get('title')}'")
        create_response = books_client.create_book(new_book_payload)

        logger.info(f"Create book status code: {create_response.status_code}")
        assert create_response.status_code in (HTTPStatus.OK, HTTPStatus.CREATED)

        created_book = create_response.json()
        created_id = created_book.get("id")
        logger.info(f"Created book id from response: {created_id}")
        assert created_id is not None

        # Get again — API returns static data, so we only check 200, not values
        logger.info(f"Requesting book again by id={created_id}")
        get_response = books_client.get_book(created_id)

        logger.info(f"Get after create status code: {get_response.status_code}")
        assert get_response.status_code == HTTPStatus.OK

        retrieved_book = get_response.json()
        logger.info(
            "Retrieved book basic info: "
            f"id={retrieved_book.get('id')}, title='{retrieved_book.get('title')}'"
        )
        assert "id" in retrieved_book
        assert "title" in retrieved_book

    def test_update_book_title(self, books_client, new_book_payload):
        """
        Update a book title. Fake API does NOT persist changes.
        Validate only status codes.
        """
        logger.info("Creating a book to update later")
        create_response = books_client.create_book(new_book_payload)
        logger.info(f"Create book status code: {create_response.status_code}")
        assert create_response.status_code in (HTTPStatus.OK, HTTPStatus.CREATED)

        created_book = create_response.json()
        book_id = created_book["id"]
        logger.info(f"Book created with id={book_id} and title='{created_book.get('title')}'")

        # Update title
        updated_payload = created_book.copy()
        updated_payload["title"] = created_book.get("title", "") + " - Updated"
        logger.info(f"Updating book id={book_id} to new title='{updated_payload['title']}'")

        update_response = books_client.update_book(book_id, updated_payload)
        logger.info(f"Payload sent: {updated_payload}")
        logger.info(f"Update book status code: {update_response.status_code}")
        logger.info(f"Update book response body: {update_response.text}")
        assert update_response.status_code in (HTTPStatus.OK, HTTPStatus.NO_CONTENT)

    def test_delete_book(self, books_client, new_book_payload):
        """
        Delete a book. Fake API does NOT remove it.
        Validate only delete status code.
        """
        logger.info("Creating a book to delete")
        create_response = books_client.create_book(new_book_payload)
        logger.info(f"Create book status code: {create_response.status_code}")
        assert create_response.status_code in (HTTPStatus.OK, HTTPStatus.CREATED)

        created_book = create_response.json()
        book_id = created_book["id"]
        logger.info(f"Book created with id={book_id}, preparing to delete it")

        delete_response = books_client.delete_book(book_id)
        logger.info(f"Delete book status code: {delete_response.status_code}")
        assert delete_response.status_code in (
            HTTPStatus.OK,
            HTTPStatus.NO_CONTENT,
        )

        # Fake API returns 200 even after delete — so only validate GET returns 200
        logger.info(f"Requesting book id={book_id} after delete call")
        get_response = books_client.get_book(book_id)
        logger.info(f"Get after delete status code: {get_response.status_code}")
        assert get_response.status_code == HTTPStatus.OK
