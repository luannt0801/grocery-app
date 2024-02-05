"""Login and create new acc module."""
import tkinter as tk

import admin_window
import src.customer_window as customer_window
import db_manager as db
import my_config

from PIL import Image, ImageTk

# Module Constants:
LOGIN_WINDOW_SIZE = "300x200"
FALSE_LOG_IN_VALUE = -1

class LoginWindow:
    """Login and create new acc window."""

    def __init__(self, master):
        """Creates login window."""
        self.master = master
        self.master.title(my_config.APP_NAME)
        self.master.geometry(LOGIN_WINDOW_SIZE)
        self.master.configure(bg=my_config.BACKGROUND)
        self.frame = tk.Frame(self.master, bg=my_config.BACKGROUND, bd=15)

        # it contains error messages, for example not all entry are filled.
        self.error_label = tk.Label()

        # class entries
        self.login_entry = None
        self.password_entry = None
        self.name_entry = None
        self.phone_entry = None
        self.email_entry = None

    def initialize_login_window(self):
        """Initializing login window."""
        if self.frame:
            self.frame.destroy()
        self.frame = tk.Frame(self.master, bg=my_config.BACKGROUND, bd=15)

        # login, password label and entry
        login_label = tk.Label(self.frame, bg=my_config.BACKGROUND, text='login:')
        login_label.grid(row=0, column=0)
        password_label = tk.Label(self.frame, bg=my_config.BACKGROUND, text='password:')
        password_label.grid(row=1, column=0)
        self.login_entry = tk.Entry(self.frame, bg=my_config.FOREGROUND, width=18)
        self.login_entry.grid(row=0, column=1)
        self.password_entry = tk.Entry(self.frame, show='*', bg=my_config.FOREGROUND, width=18)
        self.password_entry.grid(row=1, column=1)

        # buttons
        login_button = tk.Button(self.frame, text='Log in', bg=my_config.FOREGROUND,
                                 command=self.login, width=16)
        login_button.grid(row=3, column=1, pady=(10, 0))
        create_button = tk.Button(self.frame, text='Create new account',
                                  bg=my_config.FOREGROUND, command=self.create_account, width=16)
        create_button.grid(row=4, column=1)
        self.frame.pack()

    def login(self):
        """Method that runs admin/customer, depending on permissions"""
        # deleting error label from last add_order call, if it exists
        if self.error_label:
            self.error_label.destroy()

        # checking if all required entries are filled
        if not self.login_entry.get():
            self.error_label = tk.Label(self.frame, text="login missing",
                                        fg=my_config.ERROR_FOREGROUND, bg=my_config.BACKGROUND)
            self.error_label.grid(row=2, column=1)
        elif not self.password_entry.get():
            self.error_label = tk.Label(self.frame, text="password missing",
                                        fg=my_config.ERROR_FOREGROUND, bg=my_config.BACKGROUND)
            self.error_label.grid(row=2, column=1)

        else:
            my_config.MY_ID, perm = db.customer_perm(self.login_entry.get(), self.password_entry.get())
            if perm == FALSE_LOG_IN_VALUE or my_config.MY_ID == FALSE_LOG_IN_VALUE:
                self.error_label = tk.Label(self.frame, text="try again..",
                                            fg=my_config.ERROR_FOREGROUND, bg=my_config.BACKGROUND)
                self.error_label.grid(row=2, column=1)
            elif perm == my_config.ADMIN_PERM:
                self.admin_app()
            else:
                self.customer_app()

    def create_account(self):
        """Initializes window for creating new accounts."""
        self.frame.destroy()
        self.frame = tk.Frame(self.master, bg=my_config.BACKGROUND)
        self.frame.pack()

        # Create text box labels for Customers
        login_label = tk.Label(self.frame, text='login:', bg=my_config.BACKGROUND)
        login_label.grid(row=0, column=0, pady=(10, 0), sticky=tk.E)
        password_label = tk.Label(self.frame, text='password:', bg=my_config.BACKGROUND)
        password_label.grid(row=1, column=0, sticky=tk.E, )
        name_label = tk.Label(self.frame, text='name:', bg=my_config.BACKGROUND)
        name_label.grid(row=2, column=0, sticky=tk.E)
        phone_label = tk.Label(self.frame, text='phone:', bg=my_config.BACKGROUND)
        phone_label.grid(row=3, column=0, sticky=tk.E)
        email_label = tk.Label(self.frame, text='email:', bg=my_config.BACKGROUND)
        email_label.grid(row=4, column=0, sticky=tk.E)

        # Create Entry box for Customers
        self.login_entry = tk.Entry(self.frame, width=18, bg=my_config.FOREGROUND)
        self.login_entry.grid(row=0, column=1, pady=(10, 0))
        self.password_entry = tk.Entry(self.frame, width=18, show='*', bg=my_config.FOREGROUND)
        self.password_entry.grid(row=1, column=1)
        self.name_entry = tk.Entry(self.frame, width=18, bg=my_config.FOREGROUND)
        self.name_entry.grid(row=2, column=1)
        self.phone_entry = tk.Entry(self.frame, width=18, bg=my_config.FOREGROUND)
        self.phone_entry.grid(row=3, column=1)
        self.email_entry = tk.Entry(self.frame, width=18, bg=my_config.FOREGROUND)
        self.email_entry.grid(row=4, column=1)

        # buttons
        login_button = tk.Button(self.frame, text='create', command=self.create_account_db,
                                 width=16, bg=my_config.FOREGROUND)
        login_button.grid(row=6, column=0, pady=(20, 0))
        create_button = tk.Button(self.frame, text='Cancel', command=self.initialize_login_window,
                                  width=16, bg=my_config.FOREGROUND)
        create_button.grid(row=6, column=1, pady=(20, 0))

    def create_account_db(self):
        """Create new account if all required entries are filled."""
        # deleting missing label from last add_order call, if it exists
        if self.error_label:
            self.error_label.destroy()

        # checking if all required entries are filled.
        # checking if all required entries are filled.
        if not self.login_entry.get():
            self.error_label = tk.Label(self.frame, text="'login' missing",
                                        fg=my_config.ERROR_FOREGROUND, bg=my_config.BACKGROUND)
            self.error_label.grid(row=5, column=1)
        elif len(self.password_entry.get()) < 6:
            self.error_label = tk.Label(self.frame, text="minimum password length is 6",
                                        fg=my_config.ERROR_FOREGROUND, bg=my_config.BACKGROUND)
            self.error_label.grid(row=5, column=1)
        elif not self.name_entry.get():
            self.error_label = tk.Label(self.frame, text="'name' missing",
                                        fg=my_config.ERROR_FOREGROUND, bg=my_config.BACKGROUND)
            self.error_label.grid(row=5, column=1)
        elif not self.email_entry.get():
            self.error_label = tk.Label(self.frame, text="'email' missing",
                                        fg=my_config.ERROR_FOREGROUND, bg=my_config.BACKGROUND)
            self.error_label.grid(row=5, column=1)
        elif self.phone_entry.get() and not my_config.is_integer(self.phone_entry.get()):
            self.error_label = tk.Label(self.frame, text="wrong phone number",
                                        fg=my_config.ERROR_FOREGROUND, bg=my_config.BACKGROUND)
            self.error_label.grid(row=5, column=1)

        else:
            # checking if customer is in DB
            exist = db.is_customer_exists(self.login_entry.get(), self.email_entry.get())
            if exist == my_config.CUSTOMER_EMAIL:
                self.error_label = tk.Label(self.frame, text="Email exists.".format(exist),
                                            fg=my_config.ERROR_FOREGROUND, bg=my_config.BACKGROUND)
                self.error_label.grid(row=5, column=1)

            elif exist == my_config.CUSTOMER_LOGIN:
                self.error_label = tk.Label(self.frame, text="Login exists.".format(exist),
                                            fg=my_config.ERROR_FOREGROUND, bg=my_config.BACKGROUND)
                self.error_label.grid(row=5, column=1)
            else:
                db.add_customer(self.login_entry.get(), self.password_entry.get(),
                                self.name_entry.get(), self.phone_entry.get(),
                                self.email_entry.get())
                self.frame.destroy()
                application = LoginWindow(self.master)
                application.initialize_login_window()

    def admin_app(self):
        """Initializing Admin window."""
        self.frame.destroy()
        application = admin_window.CustomersMenu(self.master)
        application.initialize_menu()

    def customer_app(self):
        """Initializing Customer window."""
        self.frame.destroy()
        application = customer_window.CustomerApp(self.master)
        application.initialize_main_buttons()
