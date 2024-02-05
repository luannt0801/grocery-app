"""Unit tests for admin_window module."""
import tkinter as tk
import unittest

import admin_window


class ProductsMenuTest(unittest.TestCase):

    def setUp(self):
        root = tk.Tk()
        self.application = admin_window.ProductsMenu(root)
        self.application.initialize_menu()

    def test_clear_product_entries(self):
        self.application.product_name_entry.insert(tk.END, "LG G6")
        self.application.product_price_entry.insert(tk.END, "123")
        self.application.in_stock_entry.insert(tk.END, "5")
        self.application.description_entry.insert(tk.END, "safasf")

        self.application.clear_product_entries()

        self.assertFalse(self.application.product_name_entry.get())
        self.assertFalse(self.application.product_price_entry.get())
        self.assertFalse(self.application.in_stock_entry.get())
        self.assertFalse(self.application.description_entry.get())

    def test_search_product(self):
        self.application.clear_product_entries()
        self.application.product_name_entry.insert(tk.END, "LG G6")
        self.application.search_product()  # inserts into tree searched values

        child = self.application.product_tree.get_children()  # product name is unique
        self.assertTrue(self.application.product_tree.item(child)['values'][1] == "LG G6")


class CustomersMenuTest(unittest.TestCase):

    def setUp(self):
        root = tk.Tk()
        self.application = admin_window.CustomersMenu(root)
        self.application.initialize_menu()

    def test_clear_customer_entries(self):
        self.application.name_entry.insert(tk.END, "asdasd")
        self.application.login_entry.insert(tk.END, "123123")
        self.application.email_entry.insert(tk.END, "asdasd@gmail.com")
        self.application.phone_entry.insert(tk.END, "123123123")
        self.application.perm_entry.insert(tk.END, "0")

        self.application.clear_customer_entries()

        self.assertFalse(self.application.name_entry.get())
        self.assertFalse(self.application.login_entry.get())
        self.assertFalse(self.application.email_entry.get())
        self.assertFalse(self.application.phone_entry.get())
        self.assertFalse(self.application.perm_entry.get())

    def test_search_customer(self):
        self.application.clear_customer_entries()
        self.application.login_entry.insert(tk.END, "admin")
        self.application.search_customer()  # inserts into tree searched values

        child = self.application.customers_tree.get_children()  # login is unique
        self.assertTrue(self.application.customers_tree.item(child)['values'][1] == "admin")


class OrdersMenuTest(unittest.TestCase):

    def setUp(self):
        root = tk.Tk()
        self.application = admin_window.OrdersMenu(root)
        self.application.initialize_menu()

    def test_clear_entries(self):
        self.application.id_customer_entry.insert(tk.END, "1")
        self.application.id_product_entry.insert(tk.END, "1")
        self.application.quantity_entry.insert(tk.END, "5")
        self.application.payment_status_entry.insert(tk.END, "1")
        self.application.send_status_entry.insert(tk.END, "0")
        self.application.location_entry.insert(tk.END, "Jędrychowa chatka")

        self.application.initialize_menu()

        self.assertFalse(self.application.id_customer_entry.get())
        self.assertFalse(self.application.id_product_entry.get())
        self.assertFalse(self.application.quantity_entry.get())
        self.assertFalse(self.application.payment_status_entry.get())
        self.assertFalse(self.application.send_status_entry.get())
        self.assertFalse(self.application.location_entry.get())

    def test_search_order(self):
        self.application.send_status_entry.insert(tk.END, "1")
        self.application.search_order()  # inserts into tree searched values

        for child in self.application.order_tree.get_children():
            self.assertTrue(self.application.order_tree.item(child)['values'][3] == 1)


if __name__ == '__main__':
    unittest.main()
