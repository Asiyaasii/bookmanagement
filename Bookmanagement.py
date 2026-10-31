
import mysql.connector


class Book_db:

    def __init__(self):
        try:
            self.con = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="bookstore",autocommit=True

            )

            print("Database connected successfully!")

        except mysql.connector.Error as e:
            print("Database connection failed:", e)
            self.con = None

    # 1. INSERT BOOK
    def create(self, book_id, title, author, category, price, stock):
        if self.con is None:
            return

        cursor = None
        try:
            cursor = self.con.cursor()

            query = """
            INSERT INTO books
            (book_id, title, author, category, price, stock)
            VALUES (%s, %s, %s, %s, %s, %s)
            """

            data = (book_id, title, author, category, price, stock)

            cursor.execute(query, data)
            self.con.commit()

            print("Book added successfully!")

        except mysql.connector.Error as e:
            self.con.rollback()
            print("Failed to create book:", e)

        finally:
            if cursor:
                cursor.close()

    # 2. DISPLAY ALL BOOKS
    def read(self):
        if self.con is None:
            return

        cursor = None
        try:
            cursor = self.con.cursor()

            cursor.execute("SELECT * FROM books")
            records = cursor.fetchall()

            if records:
                for row in records:
                    print(row)
            else:
                print("No records found.")

        except mysql.connector.Error as e:
            print("Failed to read books:", e)

        finally:
            if cursor:
                cursor.close()

    # 3. SEARCH BOOK BY ID
    def retrieve(self, book_id):
        if self.con is None:
            return

        cursor = None
        try:
            cursor = self.con.cursor()

            query = "SELECT * FROM books WHERE book_id = %s"
            cursor.execute(query, (book_id,))

            record = cursor.fetchone()

            if record:
                print("Book found:", record)
            else:
                print("Book not found.")

        except mysql.connector.Error as e:
            print("Failed to retrieve book:", e)

        finally:
            if cursor:
                cursor.close()

    # 4. UPDATE BOOK PRICE
    def update(self, book_id, price):
        if self.con is None:
            return

        cursor = None
        try:
            cursor = self.con.cursor()

            query = """
            UPDATE books
            SET price = %s
            WHERE book_id = %s
            """

            cursor.execute(query, (price, book_id))
            self.con.commit()

            print("Number of records updated:", cursor.rowcount)

        except mysql.connector.Error as e:
            self.con.rollback()
            print("Failed to update price:", e)

        finally:
            if cursor:
                cursor.close()

    # 5. DELETE BOOK
    def delete(self, book_id):
        if self.con is None:
            return

        cursor = None
        try:
            cursor = self.con.cursor()

            query = "DELETE FROM books WHERE book_id = %s"
            cursor.execute(query, (book_id,))
            self.con.commit()

            if cursor.rowcount > 0:
                print("Book deleted successfully!")
            else:
                print("Book not found.")

        except mysql.connector.Error as e:
            self.con.rollback()
            print("Failed to delete book:", e)

        finally:
            if cursor:
                cursor.close()

    # 6. BOOKS BELOW RS.500
    def below_500(self):
        if self.con is None:
            return

        cursor = None
        try:
            cursor = self.con.cursor()

            query = "SELECT * FROM books WHERE price < 500"
            cursor.execute(query)

            records = cursor.fetchall()

            if records:
                for row in records:
                    print(row)
            else:
                print("No books found below Rs.500.")

        except mysql.connector.Error as e:
            print("Error:", e)

        finally:
            if cursor:
                cursor.close()

    # 7. CATEGORY-WISE COUNT
    def category_count(self):
        if self.con is None:
            return

        cursor = None
        try:
            cursor = self.con.cursor()

            query = """
            SELECT category, COUNT(*)
            FROM books
            GROUP BY category
            """

            cursor.execute(query)
            records = cursor.fetchall()

            for row in records:
                print("Category:", row[0], "Count:", row[1])

        except mysql.connector.Error as e:
            print("Error:", e)

        finally:
            if cursor:
                cursor.close()

    # 8. SECOND HIGHEST DISTINCT PRICE
    def second_highest(self):
        if self.con is None:
            return

        cursor = None
        try:
            cursor = self.con.cursor()

            query = """
            SELECT DISTINCT price
            FROM books
            ORDER BY price DESC
            LIMIT 1 OFFSET 1
            """

            cursor.execute(query)
            record = cursor.fetchone()

            if record:
                print("Second highest price:", record[0])
            else:
                print("Second highest price does not exist.")

        except mysql.connector.Error as e:
            print("Error:", e)

        finally:
            if cursor:
                cursor.close()

    # 9. PURCHASE BOOK
    def purchase(self, book_id, quantity):
        if self.con is None:
            return

        cursor = None
        try:
            if quantity <= 0:
                print("Invalid quantity.")
                return

            cursor = self.con.cursor()

            self.con.start_transaction()

            query = """
            SELECT stock FROM books
            WHERE book_id = %s
            FOR UPDATE
            """

            cursor.execute(query, (book_id,))
            record = cursor.fetchone()

            if record is None:
                self.con.rollback()
                print("Book not found.")
                return

            available_stock = record[0]

            if available_stock >= quantity:

                update_query = """
                UPDATE books
                SET stock = stock - %s
                WHERE book_id = %s
                """

                cursor.execute(update_query, (quantity, book_id))
                self.con.commit()

                print("Purchase successful!")
                print("Remaining stock:",
                      available_stock - quantity)

            else:
                self.con.rollback()
                print("Insufficient stock!")
                print("Available stock:", available_stock)

        except mysql.connector.Error as e:
            self.con.rollback()
            print("Purchase failed:", e)

        finally:
            if cursor:
                cursor.close()

    # CLOSE DATABASE
    def close(self):
        if self.con is not None and self.con.is_connected():
            self.con.close()
            print("Database connection closed.")


# CREATE OBJECT
b = Book_db()

if b.con is not None:

    while True:

        print("\n===== ONLINE BOOK MANAGEMENT SYSTEM =====")
        print("1. Insert New Book")
        print("2. Display All Books")
        print("3. Search Book by ID")
        print("4. Update Book Price")
        print("5. Delete Book")
        print("6. Display Books Below Rs.500")
        print("7. Category-wise Book Count")
        print("8. Second Highest Book Price")
        print("9. Purchase Book")
        print("10. Exit")

        try:
            ch = int(input("Enter your choice: "))

            if ch == 1:
                book_id = int(input("Enter Book ID: "))
                title = input("Enter Title: ")
                author = input("Enter Author: ")
                category = input("Enter Category: ")
                price = float(input("Enter Price: "))
                stock = int(input("Enter Stock: "))

                b.create(book_id, title, author,
                         category, price, stock)

            elif ch == 2:
                b.read()

            elif ch == 3:
                book_id = int(input("Enter Book ID: "))
                b.retrieve(book_id)

            elif ch == 4:
                book_id = int(input("Enter Book ID: "))
                price = float(input("Enter New Price: "))
                b.update(book_id, price)

            elif ch == 5:
                book_id = int(input("Enter Book ID: "))
                b.delete(book_id)

            elif ch == 6:
                b.below_500()

            elif ch == 7:
                b.category_count()

            elif ch == 8:
                b.second_highest()

            elif ch == 9:
                book_id = int(input("Enter Book ID: "))
                quantity = int(input("Enter Quantity: "))
                b.purchase(book_id, quantity)

            elif ch == 10:
                print("Exiting program...")
                break

            else:
                print("Invalid choice!")

        except ValueError:
            print("Please enter valid input.")

    b.close()
