import sys
from services.books import BooksDB
from services.users import UsersDB
from services.check import CheckoutDB

def main_menu():
    print("Hey there! Welcome to the world's first online library Management system! Here you can manage your whole library from adding books to checking them out to your customers! 📚")
    print("So what do you want to do today? 🤔")
    print("1. Update Books in the library 📚")
    print("2. Update Users in the library 👤")
    print("3. Update Checkouts in the library 📚👤")
    print("-1. I am done for now. Exit the system.")
    choice = input("Enter choice: ")
    return choice

def books_menu():
    print("1. Add a Book in the library")
    print("2. List Books in the library")
    print("3. Delete a Book from the library")
    print("4. Update Book details")
    print("5. Search Book")
    print("-1. Exit")
    choice = input("Enter choice: ")
    return choice

def users_menu():
    print("1. Add a User")
    print("2. List Users")
    print("3. Delete a User")
    print("4. Update User details")
    print("5. Search User")
    print("-1. Exit")
    choice = input("Enter choice: ")
    return choice

def checkout_menu():
    print("1. Checkout a Book")
    print("2. Return a Book")
    print("3. Update Checkout details")
    print("4. Search Checkout")
    print("5. List Checkouts")
    print("-1. Exit")
    choice = input("Enter choice: ")
    return choice

def main():
    try:
        book_management = BooksDB()
        user_management = UsersDB()
        checkout_management = CheckoutDB()

        book_mapping = {
            '1': book_management.add_book,
            '2': book_management.list_books,
            '3': book_management.delete_book,
            '4': book_management.update_book_details,
            '5': book_management.search_book
        }

        user_mapping = {
            '1': user_management.add_user,
            '2': user_management.list_users,
            '3': user_management.remove_user,
            '4': user_management.update_user_details,
            '5': user_management.search_user
        }

        checkout_mapping = {
            '1': checkout_management.checkout,
            '2': checkout_management.return_book,
            '3': checkout_management.update_checkout,
            '4': checkout_management.search,
            '5': checkout_management.list_checkouts
        }

        choice_mapping = {
            '1': {"menu":books_menu, "mapping":book_mapping},
            '2': {"menu":users_menu, "mapping":user_mapping},
            '3': {"menu":checkout_menu, "mapping":checkout_mapping}
        }

        while True:
            choice = main_menu()
            if choice == '-1':
                break
            elif choice in choice_mapping:
                while True:
                    menu, mapping = choice_mapping[choice].values()
                    sub_choice = menu()

                    if sub_choice == '-1':
                        break
                    
                    if sub_choice in mapping:
                        mapping[sub_choice]()
                    else:
                        print("Invalid choice, please try again.")
            
            else:
                print("Invalid choice, please try again.")
    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
