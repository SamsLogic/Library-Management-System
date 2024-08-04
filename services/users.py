from typing import Union
import os

import pandas as pd

from services.db import DB
from models.user import AddUser, DeleteUser, User

from config.config import USERS_STORAGE_FILE_PATH, USERS_STORAGE_FILE_NAME
from config.log import db_logger

class UsersDB(DB):
    def __init__(self, file_path = os.path.join(USERS_STORAGE_FILE_PATH, f"{USERS_STORAGE_FILE_NAME}")):
        self.file_path = file_path
        self.logger = db_logger.getChild("UsersDB")
        self.columns = list(User.model_fields.keys())
        super().__init__(columns=self.columns)

    def check_user_id(self, user_id: int) -> bool:
        """
        Function to check if the user with the given user_id exists in the storage

        Args:
            user_id (int): The user_id of the user

        Returns:
            bool: True if the user exists, False otherwise
        """
        try:
            if len(self._search(file_path=self.file_path, key="user_id", val=user_id)) == 0:
                return False
            return True
        except Exception as e:
            self.logger.error(f"Error searching user in storage: {e}")
            raise e

    def update_checkout_status(self, user_id: int, status: bool) -> None:
        """
        Function to update the checkout status of a user in the storage

        Args:
            user_id (int): The user_id of the user
            status (bool): The checkout status

        Returns:
            None
        """
        try:
            user = User(**self._search(file_path=self.file_path, key="user_id", val=user_id).to_dict(orient="records")[0])
            
            # Check if the user is already checked out
            if user.is_checked_out == status:
                self.logger.warning("User is already checked out.")
                return
            
            # Update the checkout status of the user
            user.is_checked_out = status

            # Update the user in the storage
            self._update(file_path=self.file_path, key_col="user_id", data=user)
            self.logger.info("User checkout status updated.")
        except Exception as e:
            self.logger.error(f"Error updating user checkout status: {e}")
            raise e

    def add_user(self) -> None:
        """
        Function to add a user to the library

        Args:
            Takes input from the user

        Returns:
            None
        """
        try:
            user = AddUser(**self._ask_for_input(AddUser.model_fields))
            
            # Check if the user_id already exists
            if self.check_user_id(user_id=user.user_id):
                self.logger.warning("User ID already exists in storage. Cannot add user.")
                return

            # Add the user to the storage
            self._add(file_path=self.file_path, data=user)
            self.logger.info("User added.")
        except Exception as e:
            self.logger.error(f"Error adding user to storage: {e}")
            raise e
    
    def remove_user(self) -> None:
        """
        Function to remove a user from the library

        Args:
            Takes input from the user

        Returns:
            None
        """
        try:
            user = DeleteUser(**self._ask_for_input(DeleteUser.model_fields))

            # Check if the user_id exists in the storage
            if not self.check_user_id(user_id=user.user_id):
                self.logger.warning("User ID does not exist in storage. Cannot remove user.")
                return
            
            # Check if the user has a book checked out
            if self._search(file_path=self.file_path, key="user_id", val=user.user_id)['is_checked_out'].values[0]:
                self.logger.warning("User has a book checked out. Cannot remove user.")
                return
            
            # Remove the user from the storage
            self._delete(file_path=self.file_path, data=user)
            self.logger.info("User removed.")
        except Exception as e:
            self.logger.error(f"Error removing user from storage: {e}")
            raise e
    
    def update_user_details(self) -> None:
        """
        Function to update the details of a user in the library

        Args:
            Takes input from the user

        Returns:
            None
        """
        try:
            user = User(**self._ask_for_input(User.model_fields))
            
            # Check if the user_id exists in the storage
            if not self.check_user_id(user_id=user.user_id):
                self.logger.warning("User ID does not exist in storage. Cannot update user.")
                return
            
            # Update the user in the storage
            self._update(file_path=self.file_path, key_col="user_id", data=user)
            self.logger.info("User updated.")
        except Exception as e:
            self.logger.error(f"Error updating user in storage: {e}")
            raise e
    
    def search_user(self, print_output: bool = True) -> Union[None, pd.DataFrame]:
        """
        Function to search for a user in the library

        Args:
            print_output (bool): Whether to print the output or not
            Takes input from the user

        Returns:
            Union[None, pd.DataFrame]: The search results if print_output is False
        """
        try:
            user = User(**self._ask_for_input(User.model_fields))

            # search the user in the storage based on the input if it exists based on user_id or name
            if user.user_id:
                if not print_output:
                    return self._search(file_path=self.file_path, key="user_id", val=user.user_id)
                print(self._search(file_path=self.file_path, key="user_id", val=user.user_id))
            if user.name:
                if not print_output:
                    return self._search(file_path=self.file_path, key="name", val=user.name)
                print(self._search(file_path=self.file_path, key="name", val=user.name))
            return
        except Exception as e:
            self.logger.error(f"Error searching user in storage: {e}")
            raise e
    
    def list_users(self, print_output: bool = True) -> Union[None, pd.DataFrame]:
        """
        Function to list all the users in the library

        Args:
            print_output (bool): Whether to print the output or not

        Returns:
            Union[None, pd.DataFrame]: The list of users if print_output is False
        """
        try:
            if not print_output:
                return self._list(file_path=self.file_path)
            print(self._list(file_path=self.file_path))
        except Exception as e:
            self.logger.error(f"Error listing users in storage: {e}")
            raise e