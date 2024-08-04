from typing import Union
import os

import pandas as pd

from services.db import DB
from models.book import Book, AddBook, DeleteBook

from config.config import BOOKS_STORAGE_FILE_NAME, BOOKS_STORAGE_FILE_PATH
from config.log import db_logger

class BooksDB(DB):
    def __init__(self, file_path = os.path.join(BOOKS_STORAGE_FILE_PATH, f"{BOOKS_STORAGE_FILE_NAME}")):
        self.file_path = file_path
        self.logger = db_logger.getChild("BooksDB")
        self.columns = list(Book.model_fields.keys())
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

    def update_availability(self, new_book: AddBook, increase: bool = True) -> None:
        """
        Function to update the availability of a book in the storage

        Args:
            new_book (AddBook): The new book details
            increase (bool, optional): Whether to increase the availability. Defaults to True.

        Returns:
            None
        """
        try:
            # check if the book with the given isbn exists
            book = self._search(file_path=self.file_path, key="isbn", val=new_book.isbn)
            
            # if the book exists, update the availability
            if book['title'].values[0] == new_book.title and book['author'].values[0] == new_book.author:
                # if increase is True, increase the availability
                # else decrease the availability
                if increase:
                    new_book.availability += book['availability'].values[0]
                else:
                    if book['availability'].values[0] == 0:
                        self.logger.warning("Book is already unavailable. Not updating availability.")
                        return
                    new_book.availability = book['availability'].values[0] - 1
            else:
                self.logger.warning("Book details do not match. Not updating availability.")
                return

            # update the availability in the storage
            self._update(file_path=self.file_path, key_col="isbn", data=new_book)
            self.logger.info("Book availability increased.")
        except Exception as e:
            self.logger.error(f"Error increasing book availability: {e}")
            raise e

    def add_book(self) -> None:
        """
        Function to add a book to the storage

        Args:
            Takes input from the user

        Returns:
            None
        """
        try:
            book = AddBook(**self._ask_for_input(AddBook.model_fields))

            # check if the book with the given isbn already exists
            if self.check_isbn(isbn=book.isbn):
                self.update_availability(new_book=book)
                return
            
            # add the book to the storage
            self._add(file_path=self.file_path, data=book)
            self.logger.info("Book added.")
        except Exception as e:
            self.logger.error(f"Error adding book to storage: {e}")
            raise e
    
    def delete_book(self) -> None:
        """
        Function to delete a book from the storage

        Args:
            Takes input from the user

        Returns:
            None
        """
        try:
            book = DeleteBook(**self._ask_for_input(DeleteBook.model_fields))
            
            # check if the book with the given isbn exists
            if not self.check_isbn(isbn=book.isbn):
                self.logger.warning("ISBN does not exist in storage. Cannot remove book.")
                return

            # delete the book from the storage
            self._delete(file_path=self.file_path, data=book)
            self.logger.info("Book removed.")
        except Exception as e:
            self.logger.error(f"Error removing book from storage: {e}")
            raise e
    
    def update_book_details(self) -> None:
        """
        Function to update the details of a book in the storage

        Args:
            Takes input from the user

        Returns:
            None
        """
        try:
            book = Book(**self._ask_for_input(Book.model_fields))

            # check if the book with the given isbn exists
            if not self.check_isbn(isbn=book.isbn):
                self.logger.warning("ISBN does not exist in storage")
                return
            
            # update the book details in the storage
            self._update(file_path=self.file_path, key_col="isbn", data=book)
            self.logger.info("Book details updated.")
        except Exception as e:
            self.logger.error(f"Error updating book in storage: {e}")
            raise e
    
    def search_book(self, print_output: bool = True) -> Union[None, pd.DataFrame]:
        """
        Function to search for a book in the storage

        Args:
            print_output (bool, optional): Whether to print the output. Defaults to True.
            Takes input from the user
        
        Returns:
            Union[None, pd.DataFrame]: The data that was found if print_output is False
        """
        try:
            book = Book(**self._ask_for_input(Book.model_fields))

            # Individual search for isbn, title, and author
            if book.isbn:
                if not print_output:
                    return self._search(file_path=self.file_path, key="isbn", val=book.isbn)
                print(self._search(file_path=self.file_path, key="isbn", val=book.isbn))            
            
            if book.title:
                if not print_output:
                    return self._search(file_path=self.file_path, key="title", val=book.title)
                print(self._search(file_path=self.file_path, key="title", val=book.title))
            if book.author:
                if not print_output:
                    return self._search(file_path=self.file_path, key="author", val=book.author)
                print(self._search(file_path=self.file_path, key="author", val=book.author))
            return
        except Exception as e:
            self.logger.error(f"Error searching book in storage: {e}")
            raise e
    
    def list_books(self, print_output: bool = True) -> Union[None, pd.DataFrame]:
        """
        Function to list books in the storage

        Args:
            print_output (bool, optional): Whether to print the output. Defaults to True.

        Returns:
            Union[None, pd.DataFrame]: The data that was found if print_output is False
        """
        try:
            if not print_output:
                return self._list(file_path=self.file_path)
            print(self._list(file_path=self.file_path))
        except Exception as e:
            self.logger.error(f"Error listing books in storage: {e}")
            raise e