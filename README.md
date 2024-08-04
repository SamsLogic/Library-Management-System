# Library Management System

## Problem Statement
Design a library management system that can be used by a librarian to manage the books in the library. The system should be able to add books, remove books, issue books, return books, and display available books. The system should also be able to display the books issued to a particular student. The system should also be able to display the list of students who have issued a particular book.

## Design

### Classes

1. DB: Base class for the database. It contains methods to add, remove, update, and fetch data from the database.
2. BookDB: Class to manage the books in the library. It inherits from the DB class and contains methods to add, remove, update, and fetch books.
3. UserDB: Class to manage the users in the library. It inherits from the DB class and contains methods to add, remove, update, and fetch users.
3. CheckoutDB: Class to manage the checkout history of the books. It inherits from the DB class and contains methods to add, remove, update, and fetch checkout history.

### Data Validation

Pydantic is used for data validation. It ensures that the data passed to the methods is of the correct type and format. The pydanctic models used for data validation are (in the `models` directory):
1. Book: Class to validate the book data.
2. AddBook: Class to validate the data required to add a book.
3. DeleteBook: Class to validate the data required to delete a book.
4. User: Class to validate the user data.
5. AddUser: Class to validate the data required to add a user.
6. DeleteUser: Class to validate the data required to delete a user.
7. Checkout: Class to validate the checkout data.
8. Return: Class to validate the return data.

### Logging

The `logging` module is used to log the events in the system. The logs are stored in the `logs` directory as well as printed to the console.

### Error Handling

The default python Exceptions are raised when an error occurs in the system. The exceptions are caught in the main program and appropriate error messages are displayed to the user.

### User Interface

The user interface is a simple command-line interface. The user can interact with the system by entering commands.

## Functionalities

1. Book Management
    1. Add Book: Add a new book to the library.
    2. Remove Book: Remove a book from the library.
    3. Update Book: Update the details of a book in the library.
    4. Search Books: Display the list of books in the library that match the search query.
    5. List all Books: Display the list of all books in the library.

2. User Management
    1. Add User: Add a new user to the library.
    2. Remove User: Remove a user from the library. **Cannot remove a user with books issued.**
    3. Update User: Update the details of a user in the library.
    4. Search Users: Display the list of users in the library that match the search query.
    5. List all Users: Display the list of all users in the library.

3. Checkout Management
    1. Checkout Book: Issue a book to a user. **Auto increment the availability of the book and track if the user has any books issued or not**
    2. Return Book: Return a book issued to a user. **Auto decrement the availability of the book and checkout status of user if he has any books issued or not.**
    3. Update Checkout: Update the checkout details of a book issued to a user. **Can only update the user id if the user exists**
    3. Search Checkout: Display the list of books issued to a user or the list of users who have issued a particular book.
    4. List all Checkouts: Display the list of all books issued to users.

4. Other functionalities:
    1. Modular Design: The system is designed in a modular way to make it easy to extend and maintain.
    2. Easy to add new functionalities: The system is designed in a way that makes it easy to add new functionalities in the future.

## Running the Program

### Requirements

* Python 3.9.13 or higher
* Pip 24.1.2

### Setup

1. Clone the repository:
    ```bash
    git clone
    ```

2. Change the directory:
    ```bash
    cd Library-Management-System
    ```

3. Setup the virtual environment:
    ```bash
    pip install virtualenv
    python -m virtualenv venv
    ```
    * For Windows:
        ```bash
        venv\Scripts\activate
        ```
    
    * For Linux/Mac:
        ```bash
        source venv/bin/activate
        ```

4. Install the dependencies:
    ```bash
    pip install -r requirements.txt
    ```

### Running the Program

Run the main program:
```bash
python main.py
```








