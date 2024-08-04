import typing
from typing import Dict

import os
from pydantic import BaseModel
from pydantic.fields import FieldInfo

import pandas as pd

from config.log import db_logger

class DB():
    def __init__(self, columns) -> None:
        self.columns = columns
        self.logger = db_logger.getChild("DB")

    def _ask_for_input(self, args: Dict[str, FieldInfo]) -> dict:
        """
        Function to ask for input from the user based on the fields in the model

        Args:
            args (Dict[str, FieldInfo]): The fields in the pydantic model

        Returns:
            dict: The input from the user
        """
        try:
            out = {}
            # Ask for input for each field in the model
            for key, val in args.items():

                # Ask for input only if the field is required
                if val.is_required():
                    out[key] = input(f"Enter {key}: ")

                    # Convert the input to the required type
                    if isinstance(val.annotation, typing._UnionGenericAlias):
                        for a in val.annotation.__args__:
                            try:
                                out[key] = a(out[key])
                                break
                            except Exception:
                                continue
                    elif not isinstance(val.annotation, str):
                        out[key] = val.annotation(out[key])
                    
                    if out[key] == "":
                        out[key] = None
            return out
        except Exception as e:
            self.logger.error(f"Error asking for input: {e}")
            raise e

    def _load(self, file_path: str) -> pd.DataFrame:
        """
        Function to load data from a file

        Args:
            file_path (str): The path to the file

        Returns:
            pd.DataFrame: The data loaded from the file
        """
        try:
            if os.path.exists(file_path):
                return pd.read_csv(file_path)
            else:
                return pd.DataFrame(columns=self.columns)
        except Exception as e:
            self.logger.error(f"Error loading data from file {file_path}")
            raise e
        
    def _add(self, file_path: str, data: BaseModel) -> None:
        """
        Function to add data to the storage

        Args:
            file_path (str): The path to the file
            data (BaseModel): The pydantic data model to be added
        
        Returns:
            None
        """
        try:
            df = self._load(file_path=file_path)

            # convert the data to a DataFrame object
            new_data = data.model_dump()
            new_data = {k: [v] for k, v in new_data.items()}
            new_data = pd.DataFrame(new_data)

            # add the data to the storage
            df = pd.concat([df, new_data], ignore_index=True)
            df.to_csv(file_path, index=False)
        except Exception as e:
            self.logger.error(f"Error adding data to storage: {e}")
            raise e

    def _delete(self, file_path: str, data: BaseModel) -> None:
        """
        Function to delete data from the storage

        Args:
            file_path (str): The path to the file
            data (BaseModel): The pydantic data model to be deleted

        Returns:
            None
        """
        try:
            # load the data from the storage
            df = self._load(file_path=file_path)
            
            # delete the data from the storage if it exists in the storage
            if not df.empty:
                data = data.model_dump()
                key = list(data.keys())[0]
                val = data[key]
                df = df[df[key] != val]
                df.to_csv(file_path, index=False)
            else:
                self.logger.warning(f"Storage is empty, did not delete anything: {data}")
                return

        except Exception as e:
            self.logger.error(f"Error removing data from storage: {e}")
            raise e

    def _update(self, file_path: str, key_col:str, data: BaseModel) -> None:
        """
        Function to update data in the storage

        Args:
            file_path (str): The path to the file
            key_col (str): The primary key column
            data (BaseModel): The pydantic data model to be updated

        Returns:
            None
        """
        try:
            # load the data from the storage
            df = self._load(file_path=file_path)
            
            # update the data in the storage if it exists in the storage
            if not df.empty:
                data = data.model_dump()
                primary_key_val = data[key_col]

                # update the data in the storage if it exists in the storage and is not None 
                # for each key in the data
                for key, val in data.items():
                    if key == key_col:
                        continue

                    if val is not None:
                        df.loc[df[key_col] == primary_key_val, key] = val
                df.to_csv(file_path, index=False)
            else:
                self.logger.error(f"Storage is empty, did not update anything: {data}")

        except Exception as e:
            self.logger.error(f"Error updating data in storage: {e}")
            raise e

    def _search(self, file_path: str, key: str, val: str) -> pd.DataFrame:
        """
        Function to search data in the storage

        Args:
            file_path (str): The path to the file
            key (str): The key to search for
            val (str): The value to search for

        Returns:
            pd.DataFrame: The data that was found
        """
        try:
            # load the data from the storage
            df = self._load(file_path=file_path)

            # search for the data in the storage if it exists in the storage
            if not df.empty:
                return df[df[key] == val]
            else:
                self.logger.warning("Storage is empty, did not find anything")
                return pd.DataFrame(columns=df.columns)
        except Exception as e:
            self.logger.error(f"Error searching data in storage: {e}")
            raise e

    def _list(self, file_path: str) -> pd.DataFrame:
        """
        Function to list data in the storage
        
        Args:
            file_path (str): The path to the file

        Returns:
            pd.DataFrame: The data in the storage
        """
        try:
            return self._load(file_path=file_path)
        except Exception as e:
            self.logger.error(f"Error listing data in storage: {e}")
            raise e