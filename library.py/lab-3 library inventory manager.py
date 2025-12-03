import json
import logging
from pathlib import Path

# -------------------------------
# Logging Configuration (Task 5)
# -------------------------------
logging.basicConfig(
    filename="library.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# -------------------------------
# Task 1: Book Class
# -------------------------------
class Book:
    def __init__(self, title, author, isbn, status="available"):
        self.title = title
        self.author = author
        self.isbn = isbn
        self.status = status

    def __str__(self):
        return f"{self.title} | {self.author} | ISBN: {self.isbn} | Status: {self.status}"

    def to_dict(self):
        return {
            "title": self.title,
            "author": self.author,
            "isbn": self.isbn,
            "status": self.status
        }

    def issue(self):
        if self.status == "available":
            self.status = "issued"
            logging.info(f"Book issued: {self.title}")
            return True
        return False

    def return_book(self):
        if self.status == "issued":
            self.status = "available"
            logging.info(f"Book returned: {self.title}")
            return True
        return False


# -------------------------------
# Task 2 + Task 3: Inventory + File Handling
# -------------------------------
class LibraryInventory:
    def __init__(self):
        self.books = []

    def add_book(self, book: Book):
        self.books.append(book)
        logging.info(f"Book added: {book.title}")

    def search_by_title(self, title):
        return [b for b in self.books if title.lower() in b.title.lower()]

    def search_by_isbn(self, isbn):
        return [b for b in self.books if b.isbn == isbn]

    def display_all(self):
        for book in self.books:
            print(book)

    # SAVE WITH EXCEPTION HANDLING
    def save_to_file(self, filename="books.json"):
        try:
            with open(filename, "w") as f:
                json.dump([b.to_dict() for b in self.books], f, indent=4)
            logging.info("Books saved successfully.")
        except Exception as e:
            logging.error(f"Error saving file: {e}")

    # LOAD WITH EXCEPTION HANDLING
    def load_from_file(self, filename="books.json"):
        file = Path(filename)
        if not file.exists():
            logging.error("books.json not found. Creating new file.")
            return

        try:
            with open(filename, "r") as f:
                data = json.load(f)
                self.books = [Book(**item) for item in data]
            logging.info("Books loaded successfully.")
        except Exception as e:
            logging.error(f"Error loading file: {e}")
        finally:
            print("File read attempt completed.")


# -------------------------------
# Task 4 + Task 5: Menu Driven + Exception Handling
# -------------------------------
def menu():
    inventory = LibraryInventory()
    inventory.load_from_file()

    while True:
        print("\n===== Library Menu =====")
        print("1. Add Book")
        print("2. Issue Book")
        print("3. Return Book")
        print("4. View All Books")
        print("5. Search Book")
        print("6. Exit")

        try:
            choice = input("Enter your choice: ")
        except Exception as e:
            logging.error(f"Input error: {e}")
            print("Invalid input. Try again.")
            continue

        # Add Book
        if choice == "1":
            try:
                title = input("Title: ")
                author = input("Author: ")
                isbn = input("ISBN: ")

                book = Book(title, author, isbn)
                inventory.add_book(book)
                inventory.save_to_file()
                print("Book added successfully!")
            except Exception as e:
                logging.error(f"Error adding book: {e}")

        # Issue Book
        elif choice == "2":
            try:
                isbn = input("Enter ISBN to issue: ")
                result = inventory.search_by_isbn(isbn)

                if result:
                    if result[0].issue():
                        inventory.save_to_file()
                        print("Book issued!")
                    else:
                        print("Book already issued.")
                        logging.error("Attempted to issue already issued book.")
                else:
                    print("Book not found.")
            finally:
                logging.info("Issue book operation completed.")

        # Return Book
        elif choice == "3":
            try:
                isbn = input("Enter ISBN to return: ")
                result = inventory.search_by_isbn(isbn)

                if result:
                    if result[0].return_book():
                        inventory.save_to_file()
                        print("Book returned!")
                    else:
                        print("Book was not issued.")
                else:
                    print("Book not found.")
            finally:
                logging.info("Return book operation completed.")

        # View All Books
        elif choice == "4":
            inventory.display_all()
            logging.info("Displayed all books.")

        # Search Book
        elif choice == "5":
            try:
                title = input("Enter title to search: ")
                result = inventory.search_by_title(title)

                if result:
                    for book in result:
                        print(book)
                else:
                    print("No book found.")
            except Exception as e:
                logging.error(f"Search error: {e}")

        # Exit
        elif choice == "6":
            logging.info("Program exited by user.")
            print("Exiting program...")
            break

        else:
            print("Invalid option. Try again.")
            logging.error("Invalid menu choice entered.")


# Run Menu
if __name__ == "__main__":
    menu()
