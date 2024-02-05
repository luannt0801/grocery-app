"""DB transactions module"""
import sqlite3

import my_config

MY_CONNECTION = sqlite3.connect('dataa.db')


def initialize():
    """Create tables if not existing."""
    with MY_CONNECTION as connection:
        connection.execute("""
        CREATE TABLE IF NOT EXISTS Customers(
        id_customer   INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
        login         TEXT    NOT NULL,
        password      TEXT    NOT NULL,
        customer_name TEXT    NOT NULL,
        phone         TEXT    DEFAULT (0) NOT NULL,
        email         TEXT    NOT NULL,
        perm          INT     NOT NULL DEFAULT (0) 
        )""")

        connection.execute("""
        CREATE TABLE IF NOT EXISTS Orders(
        id_order       INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
        id_customer    INTEGER NOT NULL,
        id_product     INTEGER NOT NULL,
        quantity       INTEGER NOT NULL,
        total_price    DOUBLE  NOT NULL,
        payment_status INTEGER NOT NULL DEFAULT (0),
        send_status    INTEGER NOT NULL DEFAULT (0),
        order_date     TEXT    NOT NULL DEFAULT CURRENT_TIMESTAMP,
        location       TEXT    NOT NULL,
        
        FOREIGN KEY (id_customer) REFERENCES Customers (id_customer) 
        ON DELETE CASCADE
        ON UPDATE CASCADE,
        FOREIGN KEY (id_product) REFERENCES Products (id_product) 
        ON DELETE SET NULL
        ON UPDATE CASCADE
        )""")

        connection.execute("""
        CREATE TABLE IF NOT EXISTS Products(
        id_product    INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
        product_name  TEXT    NOT NULL,
        product_price DOUBLE  NOT NULL,
        in_stock      INTEGER NOT NULL,
        description   TEXT
        img_product   TEXT
        )""")


def is_customer_exists(login, email):
    """Returns false if not exist, or login/email depending on which exists in db."""
    with MY_CONNECTION as connection:
        cursor = connection.cursor()
        cursor.execute("SELECT exists(SELECT 1 FROM Customers WHERE login=?)", (login,))
        if cursor.fetchone()[0] == 1:
            return my_config.CUSTOMER_LOGIN

        cursor.execute("SELECT exists(SELECT 1 FROM Customers WHERE email=?)", (email,))
        if cursor.fetchone()[0] == 1:
            return my_config.CUSTOMER_EMAIL
        return my_config.CUSTOMER_ABSENT


def is_customer_id_exist(customer_id) -> bool:
    """Returns True or False depending if customer exists."""
    with MY_CONNECTION as connection:
        cursor = connection.cursor()
        cursor.execute("SELECT exists(SELECT 1 FROM Customers WHERE id_customer=?)", (customer_id,))
        return cursor.fetchone()[0] == 1


def add_customer(login, password, name, phone, email):
    """Adding new customer to DB."""
    with MY_CONNECTION as connection:
        connection.execute(
            """
            INSERT INTO Customers
            (login,password,customer_name,phone,email)
            VALUES(?,?,?,?,?)
            """,
            (login, password, name, phone, email))


def return_customers():
    """Returns list of all customers in DB."""
    with MY_CONNECTION as connection:
        cursor = connection.cursor()
        cursor.execute("SELECT id_customer, login, customer_name, phone, email, perm FROM Customers")
        return cursor.fetchall()


def return_customer(customer_id):
    """Returns single customer or None if not existing."""
    with MY_CONNECTION as connection:
        cursor = connection.cursor()
        cursor.execute(
            """
            SELECT id_customer, login, password, customer_name, phone, email, perm
            FROM Customers
            WHERE id_customer=?
            """,
            (customer_id,))
        return cursor.fetchone()


def search_customer(login="", name="", phone="", email="", permission=""):
    """Returns customers that meet at least 1 of passed args."""
    with MY_CONNECTION as connection:
        cursor = connection.cursor()
        cursor.execute(
            """
            SELECT id_customer, login, customer_name, phone, email, perm
            FROM Customers
            WHERE login=? OR customer_name=? OR phone=? OR email=? or perm=?
            """,
            (login, name, phone, email, permission))
        return cursor.fetchall()


def delete_customer(customer_id):
    """Deletes customer."""
    with MY_CONNECTION as connection:
        connection.execute("DELETE FROM Customers WHERE id_customer=?", (customer_id,))


def update_customer(customer_id, login, name, email, phone="", permission=0):
    """Update's Customer by given id."""
    with MY_CONNECTION as connection:
        connection.execute(
            """
            UPDATE Customers
            SET login=?, customer_name=?, phone=?, email=?, perm=?
            WHERE id_customer=?
            """,
            (login, name, phone, email, permission, customer_id))


def edit_customer(customer_id, password, name, email, phone):
    """Edit's Customer by given id."""
    with MY_CONNECTION as connection:
        connection.execute(
            """
            UPDATE Customers
            SET password=?, customer_name=?, phone=?, email=?
            WHERE id_customer=?
            """,
            (password, name, phone, email, customer_id))


def customer_perm(login, password):
    """Returns Customer info tuple(id, perm) or (false, -1) if not exists."""
    with MY_CONNECTION as connection:
        cursor = connection.cursor()
        cursor.execute(
            """
            SELECT id_customer, perm
            FROM Customers
            WHERE login=? and password=?
            """,
            (login, password))
        record = cursor.fetchone()
        if record is None:
            return False, -1
        return record[0], record[1]


# products ---------------------------------------------------------------


# returns true or false, whether the product exists
def is_product_exists(product_name) -> bool:
    """Returns True or False depending if product with given name exists."""
    with MY_CONNECTION as connection:
        cursor = connection.cursor()
        cursor.execute("SELECT exists(SELECT 1 FROM Products WHERE product_name=?)", (product_name,))
        return cursor.fetchone()[0] == 1


def is_product_id_exists(product_id) -> bool:
    """Returns True or False depending if product with given id exists."""
    with MY_CONNECTION as connection:
        cursor = connection.cursor()
        cursor.execute("SELECT exists(SELECT 1 FROM Products WHERE id_product=?)", (product_id,))
        return cursor.fetchone()[0] == 1


def return_product(product_id):
    """Returns product by given id."""
    with MY_CONNECTION as connection:
        cursor = connection.cursor()
        cursor.execute(
            """
            SELECT id_product, product_name, product_price, in_stock, description, img_product
            FROM Products
            WHERE id_product=?
            """,
            (product_id,))
        return cursor.fetchone()


def return_products():
    """Returns list of all products."""
    with MY_CONNECTION as connection:
        cursor = connection.cursor()
        cursor.execute(
            """
            SELECT id_product, product_name, product_price, in_stock, description, img_product
            FROM Products
            """)
        return cursor.fetchall()


def add_product(name, price, stock, description, img_product):
    """Adding new product to DB."""
    with MY_CONNECTION as connection:
        connection.execute(
            """
            INSERT INTO Products
            (product_name, product_price, in_stock, description,img_product)
            VALUES (?,?,?,?,?)
            """,
            (name, price, stock, description,img_product,)) # luan


def search_products(name='', price='', stock='', description='', img_product=''): # luan
    """Returns products that meet at least 1 of passed args."""
    with MY_CONNECTION as connection:
        cursor = connection.cursor()
        if description:
            cursor.execute(
                """
                SELECT id_product, product_name, product_price, in_stock, description, img_product
                FROM Products
                WHERE product_name=? OR product_price=? OR in_stock=? OR description=? OR img_product=?
                """,
                (name, price, stock, description,img_product)) # luan
        else:
            cursor.execute(
                """
                SELECT id_product, product_name, product_price, in_stock, description, img_product
                FROM Products
                WHERE product_name=? OR product_price=? OR in_stock=? OR img_product=?
                """,
                (name, price, stock,img_product,)) # luan
        return cursor.fetchall()


# if sec value is not passed it only check and return the value if it exists
def delete_product(product_id):
    """Delete product by it's id."""
    with MY_CONNECTION as connection:
        connection.execute("DELETE FROM Products WHERE id_product=?", (product_id,))


def update_product(product_id, name, price, stock, description, img_product):
    """Updates Customer by given id."""
    with MY_CONNECTION as connection:
        connection.execute(
            """
            UPDATE Products
            SET product_name=?, product_price=?, in_stock=?, description=?, img_product=?
            WHERE id_product=?
            """,
            (name, price, stock, description, product_id,img_product,))


def return_orders():
    """Returns list of all Orders in DB."""
    with MY_CONNECTION as connection:
        cursor = connection.cursor()
        cursor.execute(
            """
            SELECT id_order, id_customer, id_product, quantity, total_price,
            payment_status, send_status, order_date, location
            FROM Orders
            """)
        records = cursor.fetchall()
        return records


def return_product_orders(product_id):
    """Returns list of Orders that refers to passed product id."""
    with MY_CONNECTION as connection:
        cursor = connection.cursor()
        cursor.execute(
            """
            SELECT id_order, id_customer, id_product, quantity, total_price,
            payment_status, send_status, order_date, location
            FROM Orders
            Where id_product=?
            """,
            (product_id,))
        return cursor.fetchall()


def return_customer_orders(customer_id):
    """Returns list of Orders that refers to passed customer id."""
    with MY_CONNECTION as connection:
        cursor = connection.cursor()
        cursor.execute(
            """
            SELECT id_order, id_customer, id_product, quantity, total_price,
            payment_status, send_status, order_date, location
            FROM Orders
            Where id_customer=?
            """,
            (customer_id,))
        return cursor.fetchall()


def add_order(customer_id, product_id, quantity, location, payment_status=0, send_status=0):
    """Add new order to DB, return False if not enough products in stock."""
    in_stock = return_product(product_id)[3]
    if in_stock - float(quantity) < 0:
        return False

    with MY_CONNECTION as connection:
        # decreasing number of products in stock
        connection.execute("UPDATE Products SET in_stock=? WHERE id_product=?",
                           (in_stock - float(quantity), product_id))

        # adding new Order
        total_price = float(return_product(product_id)[2]) * float(quantity)
        connection.execute(
            """
            INSERT INTO Orders
            (id_customer, id_product, quantity, total_price, payment_status, send_status, location)
            VALUES(?,?,?,?,?,?,?)
            """,
            (customer_id, product_id, quantity, total_price, payment_status, send_status, location))
        return True


def orders_product_info(customer_id):
    """Returns specialized columns from Orders and products by given id.

    Returns order id, product name, quantity, total price of order."""
    with MY_CONNECTION as connection:
        cursor = connection.cursor()
        cursor.execute(
            """
            SELECT o.id_order,p.product_name,o.quantity,o.total_price
            FROM Orders AS o
            NATURAL JOIN Products AS p
            WHERE o.id_customer=?
            """,
            (customer_id,))
        return cursor.fetchall()


def delete_order(order_id):
    """Delete order by given id."""
    with MY_CONNECTION as connection:
        connection.execute("DELETE FROM Orders WHERE id_order=?", (order_id,))


def search_orders(product_id='', customer_id='', quantity='', pay='', send='', location=''):
    """Returns orders that meet at least 1 of passed args."""
    with MY_CONNECTION as connection:
        cursor = connection.cursor()
        cursor.execute(
            """
            SELECT id_order, id_customer, id_product, quantity, total_price, payment_status,
            send_status, order_date, location
            FROM Orders
            WHERE id_customer=? OR id_product=? OR quantity=? OR payment_status=? OR
            send_status=? OR location=?
             """,
            (product_id, customer_id, quantity, pay, send, location))
        return cursor.fetchall()


def return_order(order_id):
    """Return order by given id."""
    with MY_CONNECTION as connection:
        cursor = connection.cursor()
        cursor.execute(
            """
            SELECT id_order, id_customer, id_product, quantity, total_price, payment_status,
            send_status, order_date, location
            FROM Orders
            WHERE id_order=?
            """,
            (order_id,))
        return cursor.fetchone()
