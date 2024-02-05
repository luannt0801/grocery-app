"""Module contains major customer classes"""
from tkinter import messagebox
import tkinter as tk
from tkinter.ttk import Treeview

import db_manager as db
import login_window
import my_config

from PIL import Image, ImageTk


# Module Constants:
CUSTOMER_WINDOW_SIZE = "650x600"

PRODUCT_COLUMNS = ('Id', 'Product name', 'Price', 'In stock', 'Description', 'Image of Product') #luan
PRODUCT_COLUMNS_SIZE = (25, 150, 50, 50, 150, 20)

# PRODUCT_COLUMNS = ('Id', 'Product name', 'Price', 'In stock') #luan
# PRODUCT_COLUMNS_SIZE = (25, 150, 50, 50)

MY_ORDERS_COLUMNS = ('Id', 'Product name', 'Quantity', 'Total price')
MY_ORDERS_COLUMNS_SIZE = (25, 150, 60, 90)


class CustomerApp:
    """Main customer window."""

    def __init__(self, master):
        """Initializes main customer window."""
        self.master = master
        self.master.geometry(CUSTOMER_WINDOW_SIZE)
        self.master.configure(bg=my_config.BACKGROUND)
        self.master.title(my_config.APP_NAME)

        # main frames
        self.frame = tk.Frame(self.master, bg=my_config.BACKGROUND)
        self.function_frame = tk.Frame(self.master, bg=my_config.BACKGROUND)
        self.function_frame2 = tk.Frame(self.master, bg=my_config.BACKGROUND)
        self.function_frame3 = tk.Frame(self.master, bg=my_config.BACKGROUND)

        # it contains error messages, for example not all entry are filled.
        self.error_label = tk.Label()

        self.product_tree = None
        self.my_orders_tree = None
        self.location_entry = None
        self.quantity_entry = None
        self.id_product_entry = None
        self.img_product = None

    def initialize_main_buttons(self):
        """Initializes main buttons.

        Used in other functions repeatedly, that's why it's not in __init__"""
        if self.frame:
            self.frame.destroy()
        if self.function_frame:
            self.function_frame.destroy()
        if self.function_frame2:
            self.function_frame2.destroy()
        if self.function_frame3:
            self.function_frame3.destroy()

        self.frame = tk.Frame(self.master, bg=my_config.BACKGROUND)
        search_button = tk.Button(self.frame, text='List of products',
                                  bg=my_config.FOREGROUND, command=self.list_products, width=16)
        search_button.grid(row=0, column=0, pady=(10, 3))
        edit_button = tk.Button(self.frame, text='Edit account', bg=my_config.FOREGROUND,
                                command=self.account_edit, width=16)
        edit_button.grid(row=1, column=0, pady=(0, 3))
        orders_button = tk.Button(self.frame, text='My Orders', bg=my_config.FOREGROUND,
                                  command=self.my_orders, width=16)
        orders_button.grid(row=2, column=0, pady=(0, 3))
        logoff_button = tk.Button(self.frame, text='Logoff', bg=my_config.FOREGROUND,
                                  command=self.log_off, width=16)
        logoff_button.grid(row=3, column=0, pady=(0, 3))
        self.frame.pack()

    def list_products(self):
        """Lists all of the customer products under menu."""
        self.initialize_main_buttons()

        # frame for listbox
        self.function_frame = tk.Frame(self.master, bg=my_config.BACKGROUND)
        self.function_frame.pack()
        self.function_frame2 = tk.Frame(self.master, bg=my_config.BACKGROUND)
        self.function_frame2.pack()

        list_label = tk.Label(self.function_frame, text='list of products',
                              width=100, bg=my_config.BACKGROUND)
        list_label.grid(row=0, column=0, pady=(10, 0))

        # creating treeview for customers
        self.product_tree = Treeview(self.function_frame, columns=PRODUCT_COLUMNS,
                                     show='headings', height=10)
        self.product_tree.grid(row=1, column=0, padx=8)

        for column_name, width in zip(PRODUCT_COLUMNS, PRODUCT_COLUMNS_SIZE):
            self.product_tree.column(column_name, width=width, anchor=tk.CENTER)
            self.product_tree.heading(column_name, text=column_name)

        scrollbar = tk.Scrollbar(self.function_frame, orient=tk.VERTICAL)
        scrollbar.configure(command=self.product_tree.set)
        self.product_tree.configure(yscrollcommand=scrollbar)
        self.product_tree.bind('<ButtonRelease-1>', self.product_selection)

        # adding records from DB to Listbox
        records = db.return_products()
        for record in records:
            self.product_tree.insert('', tk.END, values=[record[0], record[1], record[2], record[3], record[4], record[5]])
        # print(record[5]+'\n')

        # def display_image(self, img_path):
        #     img = Image.open(img_path)
        #     img = img.resize((100, 100), Image.ANTIALIAS)  # Điều chỉnh kích thước ảnh theo nhu cầu
        #     img = ImageTk.PhotoImage(img)

        #     # Tạo label để hiển thị ảnh
        #     img_label = tk.Label(self.function_frame2, image=img, bg=my_config.BACKGROUND)
        #     img_label.image = img
        #     img_label.grid(row=4, column=0, columnspan=2, pady=10)  # Chọn vị trí và padding theo nhu cầu

        # crating labels
        id_product_label = tk.Label(self.function_frame2, text='Product ID:', bg=my_config.BACKGROUND)
        id_product_label.grid(row=0, column=0, sticky=tk.E)
        quantity_label = tk.Label(self.function_frame2, text='Quantity:', bg=my_config.BACKGROUND)
        quantity_label.grid(row=1, column=0, sticky=tk.E)
        location_label = tk.Label(self.function_frame2, text='Order location:', bg=my_config.BACKGROUND)
        location_label.grid(row=2, column=0, sticky=tk.E)
        # img_label = tk.Label(self.function_frame2, text='Image of product:', bg=my_config.BACKGROUND)  # luan
        # img_label.grid(row=3, column=0, sticky=tk.E)
        img_label = tk.Label(self.function_frame2, text='Image of product:', bg=my_config.BACKGROUND)  # luan
        print(img_label)

        # creating entry boxes
        self.id_product_entry = tk.Entry(self.function_frame2, width=30, bg=my_config.FOREGROUND)
        self.id_product_entry.grid(row=0, column=1)
        self.quantity_entry = tk.Entry(self.function_frame2, width=30, bg=my_config.FOREGROUND)
        self.quantity_entry.grid(row=1, column=1)
        self.location_entry = tk.Entry(self.function_frame2, width=30, bg=my_config.FOREGROUND)
        self.location_entry.grid(row=2, column=1)
        # self.img_product = tk.Entry(self.function_frame2, width=30, bg=my_config.FOREGROUND) # luan
        # print(self.img_product)
        # self.img_product.grid(row=3, column=1)



        # buttons
        place_order_button = tk.Button(self.function_frame2, text='Place order',
                                       bg=my_config.FOREGROUND, command=self.place_order, width=16)
        place_order_button.grid(row=4, column=0)
        details_button = tk.Button(self.function_frame2, text='details',
                                   bg=my_config.FOREGROUND, command=self.product_details, width=16)
        details_button.grid(row=4, column=1, )

    def place_order(self):
        """Place new order, if all required entries are filled."""
        if self.error_label:
            self.error_label.destroy()

        # checking if all required entries are filled properly
        if not self.id_product_entry.get():
            self.error_message("'id product' missing")
        elif not my_config.is_integer(self.quantity_entry.get()) or int(self.quantity_entry.get()) < 1:
            self.error_message("'quantity' Must be an positive integer")
        elif not self.location_entry.get():
            self.error_message("'location' missing")

        # checking if customer and product exists
        elif not db.is_customer_id_exist(my_config.MY_ID) or not db.is_product_id_exists(
                self.id_product_entry.get()):
            self.error_message("product or customer id not Exists")

        # function itself check if there is enough products, and count total price (quantity*price)
        elif db.add_order(my_config.MY_ID, self.id_product_entry.get(), self.quantity_entry.get(),
                          self.location_entry.get()):
            messagebox.showinfo("Grocery App", 'successfully added.')
            self.list_products()
        else:
            self.error_message("not enough products in stock.")

    def product_details(self):
        """show details of selected product."""
        if self.error_label:
            self.error_label.destroy()
        if self.function_frame3:
            self.function_frame3.destroy()

        if not self.id_product_entry.get():
            self.error_message("select product.")

        elif db.is_product_id_exists(self.id_product_entry.get()):

            self.function_frame3 = tk.Frame(self.master, bg=my_config.BACKGROUND)
            self.function_frame3.pack(side=tk.TOP)

            # creating Message instead of Label (description might be long)
            description = db.return_product(self.id_product_entry.get())[4]
            self.error_label = tk.Message(self.function_frame3, text="Description: {}".format(description),
                                          bg=my_config.BACKGROUND, width=300)
            self.error_label.grid(row=5, column=0)
        else:
            self.error_message("Product not exist.")

    def product_selection(self, event):
        """Adds id of selected product to designated entry."""
        try:
            if self.product_tree.selection():
                record = self.product_tree.set(self.product_tree.selection())
                print(record)
                self.id_product_entry.delete(0, tk.END)
                self.id_product_entry.insert(tk.END, record[PRODUCT_COLUMNS[0]])

        except KeyError:
            pass

    def order_selection(self, event):
        """Shows details of selected order."""
        if self.my_orders_tree.selection():
            record = self.my_orders_tree.set(self.my_orders_tree.selection())
            record = db.return_order(record[PRODUCT_COLUMNS[0]])

            if self.function_frame2:
                self.function_frame2.destroy()

            self.function_frame2 = tk.Frame(self.master, bg=my_config.BACKGROUND)
            self.function_frame2.pack(side=tk.TOP)

            # creating Message instead of Label (might be long)
            order_info = ("quantity: \t{}\ntotal_price: \t{}\npayment_status: \t{}\n"
                          "send_status: \t{}\noder_date: \t{}\nlocation: \t{}\n"
                          ).format(record[3], record[4], record[5], record[6], record[7], record[8])

            self.error_label = tk.Message(self.function_frame2, text=order_info,
                                          bg=my_config.BACKGROUND, width=300)
            self.error_label.grid(row=0, column=0)

    def account_edit(self):
        """Runs new window for editing account."""
        if self.frame:
            self.frame.destroy()
        if self.function_frame:
            self.function_frame.destroy()
        if self.function_frame2:
            self.function_frame2.destroy()
        if self.function_frame3:
            self.function_frame3.destroy()
        AccountEdit(self.master)

    def my_orders(self):
        """Creates menu with list of user orders."""
        self.initialize_main_buttons()

        self.function_frame = tk.Frame(self.master, bg=my_config.BACKGROUND)
        self.function_frame.pack()

        # creating listbox for customers
        list_label = tk.Label(self.function_frame, text='my orders:', width=100, bg=my_config.BACKGROUND)
        list_label.grid(row=0, column=0, pady=(10, 0))

        # creating treeview for customers
        self.my_orders_tree = Treeview(self.function_frame, columns=MY_ORDERS_COLUMNS,
                                       show='headings', height=10)
        self.my_orders_tree.grid(row=1, column=0)

        for column_name, width in zip(MY_ORDERS_COLUMNS, MY_ORDERS_COLUMNS_SIZE):
            self.my_orders_tree.column(column_name, width=width, anchor=tk.CENTER)
            self.my_orders_tree.heading(column_name, text=column_name)

        scrollbar = tk.Scrollbar(self.function_frame, orient=tk.VERTICAL)
        scrollbar.configure(command=self.my_orders_tree.set)
        self.my_orders_tree.configure(yscrollcommand=scrollbar)
        self.my_orders_tree.bind('<ButtonRelease-1>', self.order_selection)

        # adding records from DB to treeview
        records = db.orders_product_info(my_config.MY_ID)
        for record in records:
            self.my_orders_tree.insert('', tk.END, values=[record[0], record[1], record[2], record[3]])

        

    def error_message(self, name):
        """Shows passed message in designated place

        Used to clear code and make it more readable as it is
        called multiple times."""
        # deleting missing label from last add_order call if it exists
        if self.error_label:
            self.error_label.destroy()

        self.error_label = tk.Label(self.function_frame2, text=name, bg=my_config.BACKGROUND,
                                    fg=my_config.ERROR_FOREGROUND)
        self.error_label.grid(row=3, column=1)

    def log_off(self):
        """Returns User to logging window."""
        if self.frame:
            self.frame.destroy()
        if self.function_frame:
            self.function_frame.destroy()
        if self.function_frame2:
            self.function_frame2.destroy()
        if self.function_frame3:
            self.function_frame3.destroy()
        application = login_window.LoginWindow(self.master)
        application.initialize_login_window()


class AccountEdit:
    """Customer window for editing account."""

    def __init__(self, master):
        """Initializes editing account window."""
        self.master = master
        self.master.configure(bg=my_config.BACKGROUND)
        self.master.title(my_config.APP_NAME)
        self.master.geometry(CUSTOMER_WINDOW_SIZE)

        # label that need to be defined in __init__ so functions can check if it exist and delete it
        self.error_label = tk.Label()

        self.frame = tk.Frame(self.master, bg=my_config.BACKGROUND)
        self.frame.pack()

        # Create text box labels
        new_password_label = tk.Label(self.frame, text='new password(opt):', bg=my_config.BACKGROUND)
        new_password_label.grid(row=1, column=0, pady=(10, 0), sticky=tk.E)
        password_label = tk.Label(self.frame, text='password:', bg=my_config.BACKGROUND)
        password_label.grid(row=2, column=0, sticky=tk.E)
        name_label = tk.Label(self.frame, text='name:', bg=my_config.BACKGROUND)
        name_label.grid(row=3, column=0, pady=(4, 0), sticky=tk.E)
        phone_label = tk.Label(self.frame, text='phone:', bg=my_config.BACKGROUND)
        phone_label.grid(row=4, column=0, pady=(4, 0), sticky=tk.E)
        email_label = tk.Label(self.frame, text='email:', bg=my_config.BACKGROUND)
        email_label.grid(row=5, column=0, pady=(4, 0), sticky=tk.E)

        # Create Entry box
        self.new_password_entry = tk.Entry(self.frame, width=22, show='*', bg=my_config.FOREGROUND)
        self.new_password_entry.grid(row=1, column=1, pady=(10, 0))
        self.password_entry = tk.Entry(self.frame, width=22, show='*', bg=my_config.FOREGROUND)
        self.password_entry.grid(row=2, column=1)
        self.name_entry = tk.Entry(self.frame, width=22, bg=my_config.FOREGROUND)
        self.name_entry.grid(row=3, column=1)
        self.phone_entry = tk.Entry(self.frame, width=22, bg=my_config.FOREGROUND)
        self.phone_entry.grid(row=4, column=1)
        self.email_entry = tk.Entry(self.frame, width=22, bg=my_config.FOREGROUND)
        self.email_entry.grid(row=5, column=1)

        # Create Buttons
        self.change_button = tk.Button(self.frame, text='change', bg=my_config.FOREGROUND,
                                       command=self.set_change, width=16)
        self.change_button.grid(row=1, column=2, padx=(10, 0), pady=(10, 0))
        self.cancel_button = tk.Button(self.frame, text='Cancel', bg=my_config.FOREGROUND,
                                       command=self.exit, width=16)
        self.cancel_button.grid(row=2, column=2, padx=(10, 0))

        # getting customer info from DB
        customer_info = db.return_customer(my_config.MY_ID)
        if customer_info:
            self.name_entry.insert(tk.END, customer_info[3])
            self.phone_entry.insert(tk.END, customer_info[4])
            self.email_entry.insert(tk.END, customer_info[5])
        else:
            messagebox.showinfo("Mendiona bytes", 'ERROR: WRONG ID!!!')
            self.exit()

    def set_change(self):
        """Changes customer account details if all required entries are filled properly."""
        if self.error_label:
            self.error_label.destroy()

        # if new password entry is empty don't update it
        if 0 < len(self.new_password_entry.get()) < 6:
            self.error_message('minimum password length is 6')

        # checking if all required entries are filled properly
        elif self.password_entry.get() != db.return_customer(my_config.MY_ID)[2]:
            self.error_message('password does not match.')
        elif not self.name_entry.get():
            self.error_message('Can not update empty name.')
        elif self.phone_entry.get() and not my_config.is_integer(self.phone_entry.get()):
            self.error_message("wrong phone number.")
        elif not self.email_entry.get():
            self.error_message('Can not update empty email.')

        else:
            # if all entries are filled correctly

            if self.new_password_entry:
                # passing new password
                db.edit_customer(my_config.MY_ID, self.new_password_entry.get(), self.name_entry.get(),
                                 self.email_entry.get(),
                                 self.phone_entry.get())
            else:
                # passing old password to function (no change)
                db.edit_customer(my_config.MY_ID,
                                 db.return_customer(my_config.MY_ID)[2], self.name_entry.get(),
                                 self.email_entry.get(), self.phone_entry.get())

            self.error_message("Account has been updated.")

    def error_message(self, name):
        """Shows passed message in designated place

        Used to clear code and make it more readable as it is
        called multiple times."""
        # deleting missing label from last add_order call if it exists
        if self.error_label:
            self.error_label.destroy()

        self.error_label = tk.Label(self.frame, fg=my_config.ERROR_FOREGROUND,
                                    text=name, bg=my_config.BACKGROUND)
        self.error_label.grid(row=6, column=1)

    def exit(self):
        """Runs back main customer window."""
        self.frame.destroy()
        application = CustomerApp(self.master)
        application.initialize_main_buttons()
