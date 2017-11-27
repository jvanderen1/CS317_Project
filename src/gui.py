import tkinter as tk
from tkinter import ttk
from src.sqlconnector import SQLConnector

INTERFACE_TITLE = "Search For Available Movies"

ROWS, COLS = 2, 3


class GUI(tk.Frame):
    """Used to create a graphic user interface for searching through the database

    Components:
        :param self.root: Holds graphics root figure
        :param self.sc: SQL connector used to interact with MySQL database
        :param self.search_entry_var: Holds entry for entering search term
    """

    def __init__(self):
        """Initializes all necessary variables"""

        self.root = tk.Tk()

        # Initializes frame with root object for graphics . . .
        tk.Frame.__init__(self, self.root)
        self.root.wm_title(INTERFACE_TITLE)

        # Makes the window close button quit program . . .
        self.root.protocol("WM_DELETE_WINDOW", self.__quit_program)
        self.root['bg'] = 'white'

        self.root.resizable(True, True)     # Allows window to be resized . . .

        # Setting weights for each row . . .
        for i in range(ROWS):
            self.root.rowconfigure(i, weight=1)
        for i in range(COLS):
            self.root.columnconfigure(i, weight=1)

        # Setting ttk styling . . .
        style = ttk.Style()
        style.configure('W.TButton', background='white')
        style.configure('W.TLabelframe', background='white')

        # Variables used to keep track of options/entries in the GUI . . .
        self.search_entry_var = tk.StringVar()  # Used for keeping track of search string . . .

        # MySQL Connector used for interacting with database . . .
        self.sc = None

    # END def __init__() #

    def add_features(self):
        """Inserts every feature into the root's figure"""

        # Goes through and includes all features . . .
        self.__feature_search_tool()

        # Non-visible features here . . .
        self.sc = SQLConnector()

    # END def add_features() #

    def __feature_search_tool(self):
        """Adds components for search feature, including label, entry, and button"""

        # Title for search . . .
        search_label = ttk.Label(self.root, text="Find Movies Playing", justify='center', background='white')
        search_label.config(font=("Courier", 25))
        search_label.grid(row=0, column=0, columnspan=3)

        # Entry box for search . . .
        search_entry = ttk.Entry(self.root, textvariable=self.search_entry_var, validate="key")
        search_entry.bind("<Return>", self.__search_tool_entry)
        search_entry.config(width=40)
        search_entry.grid(row=1, column=0, columnspan=2, sticky='ew')

        # Button for search . . .
        search_button = ttk.Button(self.root, text="Search", command=self.__search_tool, style='W.TButton')
        search_button.config(width=20)
        search_button.grid(row=1, column=2, sticky='ew')

    # END def __feature_search_tool #

    def __search_tool(self):
        """Interfaces with MySQL connector to provide a search"""

        print("Entry:", self.search_entry_var.get())
        self.search_entry_var.set("")

    # END def __search_tool

    def __search_tool_entry(self, event):
        """Callback function to the real search function (holds event)

        Keyword arguments:
            :param event: Holds event data (unused)
        """

        self.__search_tool()

    # END def __search_tool_entry #

    def __quit_program(self):
        """Closes current running tkinter window"""

        self.sc.close()     # Close connection to MySQL connector . . .
        self.quit()         # Quit and destroy tkinter graphics . . .
        self.destroy()

    # END def __quit_program() #
