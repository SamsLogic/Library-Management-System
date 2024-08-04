import os
from dotenv import load_dotenv

load_dotenv(override=True)

BASE_PATH = os.getenv("BASE_PATH", os.getcwd())
BOOKS_STORAGE_FILE_NAME = os.getenv("STORAGE_FILE_NAME", "books.csv")
BOOKS_STORAGE_FILE_PATH = os.getenv("STORAGE_FILE_PATH", os.path.join(BASE_PATH, "assets"))
USERS_STORAGE_FILE_NAME = os.getenv("USERS_STORAGE_FILE_NAME", "users.csv")
USERS_STORAGE_FILE_PATH = os.getenv("USERS_STORAGE_FILE_PATH", os.path.join(BASE_PATH, "assets"))
CHECKOUT_STORAGE_FILE_NAME = os.getenv("CHECKOUT_STORAGE_FILE_NAME", "checkout.csv")
CHECKOUT_STORAGE_FILE_PATH = os.getenv("CHECKOUT_STORAGE_FILE_PATH", os.path.join(BASE_PATH, "assets"))
LOGS_FILE_PATH = os.getenv("LOGS_FILE_PATH", os.path.join(BASE_PATH, "logs"))

os.makedirs(BOOKS_STORAGE_FILE_PATH, exist_ok=True)