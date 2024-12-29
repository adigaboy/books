"""
Books API

This is a simple FastAPI application that provides a RESTful API for managing a collection of books.

## Requirements

- Python 3.7+
- FastAPI
- Uvicorn

## Installation

1. Clone the repository:
    ```bash
    git clone <repository_url>
    cd <repository_directory>
    ```

2. Create a virtual environment and activate it:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install the dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## Running the Application

Start the FastAPI application using Uvicorn:
    ```bash
    uvicorn app:app --reload
    ```

## Testing the Application

1. Install the test dependencies:
    ```bash
    pip install -r dev_requirements.txt
    ```

2. Run unittest command:
    ```bash
    python -m unittest tests.test_apis
    ```
