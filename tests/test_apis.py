
import unittest
from fastapi.testclient import TestClient
from requests.auth import HTTPBasicAuth

from app import app, db

class Tests(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.client = TestClient(app)
        return super().setUp()

class TestGetAPI(Tests):
    def test_get_book__not_found(self):
        book_isbn = 'testss'
        response = self.client.get(f'/books/{book_isbn}')
        self.assertEqual(response.status_code, 404)

    def test_get_book__success(self):
        book_isbn = 'test_book_1234'
        expected_book = {
            'isbn': book_isbn,
            'title': 'The Hobbit',
            'author': 'JRR Tolkien',
            'publisher': 'Tolkien',
            'publication_date': '1924-11-21'
        }
        db[book_isbn] = expected_book
        response = self.client.get(f'/books/{book_isbn}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), expected_book)

    def test_get_book__success__multiple_books_in_db(self):
        book_isbn = 'test_book_1234'
        expected_book = {
            'isbn': book_isbn,
            'title': 'The Hobbit',
            'author': 'JRR Tolkien',
            'publisher': 'Tolkien',
            'publication_date': '1924-11-21'
        }
        other_book = {
            'isbn': 'test_book_123123',
            'title': 'The Lord of the Rings',
            'author': 'JRR Tolkien',
            'publisher': 'Tolkien',
            'publication_date': '1944-01-21'
        }
        db[book_isbn] = expected_book
        db[other_book['isbn']] = other_book
        response = self.client.get(f'/books/{book_isbn}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), expected_book)


class TestAddAPI(Tests):
    def setUp(self):
        db.clear()
        return super().setUp()

    def test_add_book__without_auth(self):
        book_to_add = {
            'isbn': 'test_book_1234',
            'title': 'The Hobbit',
            'author': 'JRR Tolkien',
            'publisher': 'Tolkien',
            'publication_date': '1924-11-21'
        }
        response = self.client.post(f'/books', json=book_to_add)
        self.assertEqual(response.status_code, 401)

    def test_add_book__success(self):
        book_to_add = {
            'isbn': 'test_book_1234',
            'title': 'The Hobbit',
            'author': 'JRR Tolkien',
            'publisher': 'Tolkien',
            'publication_date': '1924-11-21'
        }
        response = self.client.post(f'/books', json=book_to_add, auth=HTTPBasicAuth('admin', 'admin'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), book_to_add)

    def test_add_book__already_exists(self):
        book_to_add = {
            'isbn': 'test_book_1234',
            'title': 'The Hobbit',
            'author': 'JRR Tolkien',
            'publisher': 'Tolkien',
            'publication_date': '1924-11-21'
        }
        db[book_to_add['isbn']] = book_to_add
        response = self.client.post(f'/books', json=book_to_add, auth=HTTPBasicAuth('admin', 'admin'))
        self.assertEqual(response.status_code, 400)
        self.assertEqual('Book already exists', response.json()['detail'])

    def test_add_book__success__multiple_books_in_db(self):
        book_to_add_1 = {
            'isbn': 'test_book_1234',
            'title': 'The Hobbit',
            'author': 'JRR Tolkien',
            'publisher': 'Tolkien',
            'publication_date': '1924-11-21'
        }
        book_to_add_2 = {
            'isbn': 'test_book_123123',
            'title': 'The Lord of the Rings',
            'author': 'JRR Tolkien',
            'publisher': 'Tolkien',
            'publication_date': '1944-01-21'
        }
        response = self.client.post(f'/books', json=book_to_add_1, auth=HTTPBasicAuth('admin', 'admin'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), book_to_add_1)
        response = self.client.post(f'/books', json=book_to_add_2, auth=HTTPBasicAuth('admin', 'admin'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), book_to_add_2)
