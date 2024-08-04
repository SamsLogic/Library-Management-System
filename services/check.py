from typing import Union
import os

import pandas as pd

from services.db import DB
from models.checkout import Checkout, Return
from models.book import Book
from services.books import BooksDB
from services.users import UsersDB

from config.config import CHECKOUT_STORAGE_FILE_NAME, CHECKOUT_STORAGE_FILE_PATH
from config.log import db_logger

class CheckoutDB(DB):
    def __init__(self, file_path = os.path.join(CHECKOUT_STORAGE_FILE_PATH, f"{CHECKOUT_STORAGE_FILE_NAME}")):
        self.file_path = file_path
        self.logger = db_logger.getChild("CheckoutDB")
        self.columns = list(Checkout.model_fields.keys())
        self.books_db = BooksDB()
        self.users_db = UsersDB()
        super().__init__(columns=self.columns)

    def check_isbn(self, isbn: int) -> bool:
        """
        Function to check if the book with the given isbn exists in the storage
        
        Args:
            isbn (int): The isbn of the book

        Returns:
            bool: True if the book exists, False otherwise
        """
        try:
            # check the count of the book with the given isbn
            if len(self._search(file_path=self.file_path, key="isbn", val=isbn)) == 0:
                return False
            return True
        except Exception as e:
            self.logger.error(f"Error searching book in storage: {e}")
            raise e

    def checkout(self) -> None:
        """
        Function to checkout a book from the library

        Args:
            The input from the user

        Returns:
            None
        """
        try:
            # Ask for input from the user
            checkout = Checkout(**self._ask_for_input(Checkout.model_fields))
            
            # Check if the book exists in the storage
            if not self.books_db.check_isbn(isbn=checkout.isbn):
                self.logger.warning("Book does not exist in storage. Not checking out.")
                return
            
            # Check if the book is already checked out
            if not self.users_db.check_user_id(user_id=checkout.user_id):
                self.logger.warning("User ID does not exist in storage. Not checking out.")
                return

            # Check if the book is already checked out
            if self.check_isbn(isbn=checkout.isbn):
                self.logger.warning("ISBN already exists in storage. Not checking out.")
                return
            
            book = Book(**self.books_db._search(file_path=self.books_db.file_path, key="isbn", val=checkout.isbn).to_dict(orient="records")[0])

            # Check if the book is available for checkout and update the availability
            self.books_db.update_availability(new_book=book, increase=False)

            # Check if the user is already checked out and update the status
            self.users_db.update_checkout_status(user_id=checkout.user_id, status=True)

            # Add the book to the storage
            self._add(file_path=self.file_path, data=checkout)
            self.logger.info("Book checked out.")
        except Exception as e:
            self.logger.error(f"Error adding book to storage: {e}")
            raise e
    
    def return_book(self):
        """
        Function to return a book to the library

        Args:
            The input from the user

        Returns:
            None
        """
        try:
            # Ask for input from the user
            returnb = Return(**self._ask_for_input(Return.model_fields))
            
            # Check if the book exists in the storage
            if not self.books_db.check_isbn(isbn=returnb.isbn):
                self.logger.warning("Book does not exist in storage. Cannot return.")
                return
            
            # Check if the book is already checked out
            if not self.check_isbn(isbn=returnb.isbn):
                self.logger.warning("ISBN does not exist in storage. Cannot return.")
                return
        
            checkout_details = Checkout(**self._search(file_path=self.file_path, key="isbn", val=returnb.isbn).to_dict(orient="records")[0])

            # Check if the user exists in the storage
            if not self.users_db.check_user_id(user_id=checkout_details.user_id):
                self.logger.warning("User ID does not exist in storage. Cannot return.")
                return
            
            user_with_books = self._search(file_path=self.file_path, key="user_id", val=checkout_details.user_id)
            
            book = Book(**self.books_db._search(file_path=self.books_db.file_path, key="isbn", val=returnb.isbn).to_dict(orient="records")[0])
            
            # Check if the book is available for return and update the availability
            self.books_db.update_availability(new_book=book, increase=True)

            # Check if the user is already checked out and update the status
            if len(user_with_books) == 1:
                self.users_db.update_checkout_status(user_id=checkout_details.user_id, status=False)

            # Remove the book from the storage
            self._delete(file_path=self.file_path, data=returnb)
            self.logger.info("Book returned.")
        except Exception as e:
            self.logger.error(f"Error removing book from storage: {e}")
            raise e
    
    def update_checkout(self) -> None:
        """
        Function to update the checkout details in the storage

        Args:
            Takes input from the user

        Returns:
            None
        """
        try:
            checkout = Checkout(**self._ask_for_input(Checkout.model_fields))

            # check if the book with the given isbn exists
            if not self.check_isbn(isbn=checkout.isbn):
                self.logger.warning("ISBN does not exist in storage. Cannot update.")
                return
            
            # check if the user with the given user_id exists
            if not self.users_db.check_user_id(user_id=checkout.user_id):
                self.logger.warning("User ID does not exist in storage. Cannot update.")
                return
            
            # update the book details in the storage
            self._update(file_path=self.file_path, key_col="isbn", data=checkout)
            self.logger.info("Checkout updated.")
        except Exception as e:
            self.logger.error(f"Error updating book in storage: {e}")
            raise e

    def search(self, print_output: bool = True) -> Union[None, pd.DataFrame]:
        """
        Function to search for a book in the storage

        Args:
            print_output (bool): Whether to print the output or not
            Takes input from the user

        Returns:
            Union[None, pd.DataFrame]: The search results if print_output is False
        """
        try:
            checkout = Checkout(**self._ask_for_input(Checkout.model_fields))
            
            # search the book in the storage based on the input if it exists based on isbn or user_id
            if checkout.isbn:
                if not print_output:
                    return self._search(file_path=self.file_path, key="isbn", val=checkout.isbn)
                print(self._search(file_path=self.file_path, key="isbn", val=checkout.isbn))
            if checkout.user_id:
                if not print_output:
                    return self._search(file_path=self.file_path, key="user_id", val=checkout.user_id)
                print(self._search(file_path=self.file_path, key="user_id", val=checkout.user_id))
            return
        except Exception as e:
            self.logger.error(f"Error searching book in storage: {e}")
            raise e
    
    def list_checkouts(self, print_output: bool = True) -> Union[None, pd.DataFrame]:
        """
        Function to list the checkouts in the storage

        Args:
            print_output (bool): Whether to print the output or not

        Returns:
            Union[None, pd.DataFrame]: The list of checkouts if print_output is False
        """
        try:
            if not print_output:
                return self._list(file_path=self.file_path)
            print(self._list(file_path=self.file_path))
        except Exception as e:
            self.logger.error(f"Error listing books in storage: {e}")
            raise e